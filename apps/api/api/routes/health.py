from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/v1/health")
def health(request: Request):
    return {"status": "ok", "correlation_id": request.state.correlation_id}
