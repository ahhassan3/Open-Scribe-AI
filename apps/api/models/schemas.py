from datetime import datetime

from pydantic import BaseModel, Field


class IngestAudioResponse(BaseModel):
    correlation_id: str
    transcript_id: str
    transcript_text: str
    entities_redacted: int = 0


class DeidentifyRequest(BaseModel):
    text: str


class DeidentifyResponse(BaseModel):
    correlation_id: str
    deidentified_text: str
    entities: list[dict]


class Problem(BaseModel):
    text: str
    icd10: str | None = None
    snomed: str | None = None
    confidence: float = Field(default=0.5, ge=0, le=1)


class StructuredNote(BaseModel):
    chief_complaint: str
    hpi: str
    ros: str
    assessment_plan: str
    problems: list[Problem] = Field(default_factory=list)


class NoteGenerateRequest(BaseModel):
    transcript_text: str


class NoteGenerateResponse(BaseModel):
    correlation_id: str
    note: StructuredNote
    model_info: dict[str, str | float]


class EncounterInput(BaseModel):
    start: datetime
    end: datetime
    class_code: str = Field(alias="class")
    reason: str


class PatientInput(BaseModel):
    id: str


class FhirExportRequest(BaseModel):
    note: StructuredNote
    encounter: EncounterInput
    patient: PatientInput


class FhirExportResponse(BaseModel):
    correlation_id: str
    fhir_bundle: dict
