from apps.api.models.schemas import StructuredNote
from apps.api.services.llm_orchestrator import LLMOrchestrator


class NLPEngine:
    def __init__(self, orchestrator: LLMOrchestrator | None = None) -> None:
        self.orchestrator = orchestrator or LLMOrchestrator()

    def build_structured_note(self, transcript_text: str) -> StructuredNote:
        prompt = (
            "Convert transcript into JSON with keys chief_complaint,hpi,ros,assessment_plan,problems."
            "Each problem should include text,icd10,snomed,confidence."
            f"Transcript: {transcript_text}"
        )
        response = self.orchestrator.generate_json(prompt)
        return StructuredNote.model_validate(response)
