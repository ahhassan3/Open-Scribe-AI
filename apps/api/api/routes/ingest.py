import logging

from fastapi import APIRouter, HTTPException, Request
from starlette.datastructures import UploadFile

from apps.api.core.config import get_settings
from apps.api.models.schemas import DeidentifyRequest, DeidentifyResponse, IngestAudioResponse
from apps.api.services.audio_proc import AudioProcessor
from apps.api.services.deid import Deidentifier
from apps.api.services.whisper_local import TranscriptionUnavailableError

router = APIRouter()
logger = logging.getLogger("open_scribe.audit")
audio_processor = AudioProcessor()
deidentifier = Deidentifier()


@router.post("/v1/ingest/audio", response_model=IngestAudioResponse)
async def ingest_audio(request: Request):
    settings = get_settings()
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > settings.max_multipart_memory_bytes:
        raise HTTPException(status_code=413, detail="Audio payload exceeds in-memory limit")

    form = await request.form(max_files=1, max_fields=10, max_part_size=settings.max_multipart_memory_bytes)
    file = form.get("file")
    if not isinstance(file, UploadFile):
        raise HTTPException(status_code=400, detail="Multipart field 'file' is required")

    deidentify_raw = str(form.get("deidentify", str(settings.deidentify_default))).lower()
    deidentify = deidentify_raw in {"1", "true", "yes", "on"}

    payload = await file.read()
    audio_bytes_len = len(payload)
    await file.close()
    try:
        transcript_id, transcript_text, entities_redacted = audio_processor.process_audio_bytes(payload, deidentify=deidentify)
    except TranscriptionUnavailableError as exc:
        logger.warning(
            "ingest_audio_failed",
            extra={
                "event_name": "ingest_audio_failed",
                "correlation_id": request.state.correlation_id,
                "action": "transcribe",
                "status": "failed",
                "details": {"reason": str(exc), "audio_bytes": audio_bytes_len},
            },
        )
        raise HTTPException(status_code=503, detail="Local transcription unavailable") from exc
    finally:
        payload = b""

    logger.info(
        "ingest_audio",
        extra={
            "event_name": "ingest_audio",
            "correlation_id": request.state.correlation_id,
            "action": "transcribe",
            "status": "success",
            "details": {
                "audio_bytes": audio_bytes_len,
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
