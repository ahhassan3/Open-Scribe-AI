from fastapi import FastAPI

from apps.api.api.routes.fhir import router as fhir_router
from apps.api.api.routes.health import router as health_router
from apps.api.api.routes.ingest import router as ingest_router
from apps.api.api.routes.note import router as note_router
from apps.api.core.config import get_settings
from apps.api.core.logging import configure_logging
from apps.api.middleware.hipaa_guard import HipaaGuardMiddleware

settings = get_settings()
configure_logging(settings.log_level)

app = FastAPI(title=settings.app_name)
app.add_middleware(HipaaGuardMiddleware)
app.include_router(health_router)
app.include_router(ingest_router)
app.include_router(note_router)
app.include_router(fhir_router)
