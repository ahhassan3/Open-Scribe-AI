import logging

from fastapi import APIRouter, File, Form, Request, UploadFile

from apps.api.models.schemas import DeidentifyRequest, DeidentifyResponse, IngestAudioResponse
from apps.api.services.audio_proc import AudioProcessor
from apps.api.services.deid import Deidentifier

router = APIRouter()
logger = logging.getLogger("open_scribe.audit")
audio_processor = AudioProcessor()
deidentifier = Deidentifier()


@router.post("/v1/ingest/audio", response_model=IngestAudioResponse)
async def ingest_audio(
    request: Request,
    file: UploadFile = File(...),
    deidentify: bool = Form(default=True),
):
    payload = await file.read()
    transcript_id, transcript_text, entities_redacted = audio_processor.process_audio_bytes(payload, deidentify=deidentify)
    payload = b""

    logger.info(
        "ingest_audio",
        extra={
            "event_name": "ingest_audio",
            "correlation_id": request.state.correlation_id,
            "action": "transcribe",
            "status": "success",
            "details": {
                "audio_bytes": file.size,
                "transcript_chars": len(transcript_text),
                "entities_redacted": entities_redacted,
            },
        },
    )
    return IngestAudioResponse(
        correlation_id=request.state.correlation_id,
        transcript_id=transcript_id,
        transcript_text=transcript_text,
        entities_redacted=entities_redacted,
    )


@router.post("/v1/ingest/deidentify", response_model=DeidentifyResponse)
def deidentify_text(request: Request, body: DeidentifyRequest):
    deidentified, entities = deidentifier.deidentify(body.text)
    logger.info(
        "ingest_deidentify",
        extra={
            "event_name": "ingest_deidentify",
            "correlation_id": request.state.correlation_id,
            "action": "deidentify",
            "status": "success",
            "details": {
                "input_chars": len(body.text),
                "entities_redacted": len(entities),
            },
        },
    )
    return DeidentifyResponse(
        correlation_id=request.state.correlation_id,
        deidentified_text=deidentified,
        entities=entities,
    )
