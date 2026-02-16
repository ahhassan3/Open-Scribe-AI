import logging

from fastapi import APIRouter, Request

from apps.api.models.schemas import FhirExportRequest, FhirExportResponse
from apps.api.services.fhir_mapper import build_fhir_bundle

router = APIRouter()
logger = logging.getLogger("open_scribe.audit")


@router.post("/v1/fhir/export", response_model=FhirExportResponse)
def export_fhir(request: Request, body: FhirExportRequest):
    bundle = build_fhir_bundle(body.note, body.encounter, body.patient)
    logger.info(
        "fhir_export",
        extra={
            "event_name": "fhir_export",
            "correlation_id": request.state.correlation_id,
            "action": "fhir_export",
            "status": "success",
            "details": {"entry_count": len(bundle.get("entry", []))},
        },
    )
    return FhirExportResponse(correlation_id=request.state.correlation_id, fhir_bundle=bundle)
