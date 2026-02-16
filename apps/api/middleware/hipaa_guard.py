import logging
import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from apps.api.core.config import get_settings

logger = logging.getLogger("open_scribe.audit")


class HipaaGuardMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        settings = get_settings()
        correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
        request.state.correlation_id = correlation_id

        if settings.require_api_key and request.headers.get("X-API-Key") != settings.api_key:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid API key", "correlation_id": correlation_id},
                headers={"X-Correlation-ID": correlation_id},
            )

        start = time.perf_counter()
        response = await call_next(request)
        latency_ms = int((time.perf_counter() - start) * 1000)
        response.headers["X-Correlation-ID"] = correlation_id

        logger.info(
            "request_completed",
            extra={
                "event_name": "request_completed",
                "correlation_id": correlation_id,
                "action": f"{request.method} {request.url.path}",
                "status": response.status_code,
                "details": {
                    "latency_ms": latency_ms,
                    "query_param_count": len(request.query_params),
                },
            },
        )
        return response
