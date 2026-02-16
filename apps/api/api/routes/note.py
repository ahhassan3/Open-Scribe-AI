import logging

from fastapi import APIRouter, Request

from apps.api.models.schemas import NoteGenerateRequest, NoteGenerateResponse
from apps.api.services.nlp_engine import NLPEngine

router = APIRouter()
logger = logging.getLogger("open_scribe.audit")
engine = NLPEngine()


@router.post("/v1/note/generate", response_model=NoteGenerateResponse)
def generate_note(request: Request, body: NoteGenerateRequest):
    note = engine.build_structured_note(body.transcript_text)
    logger.info(
        "note_generate",
        extra={
            "event_name": "note_generate",
            "correlation_id": request.state.correlation_id,
            "action": "note_generate",
            "status": "success",
            "details": {"transcript_chars": len(body.transcript_text), "problem_count": len(note.problems)},
        },
    )
    return NoteGenerateResponse(
        correlation_id=request.state.correlation_id,
        note=note,
        model_info={"llm": f"ollama:{engine.orchestrator.settings.llm_model}", "temperature": 0.2},
    )
