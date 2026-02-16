from datetime import datetime

from apps.api.models.schemas import EncounterInput, PatientInput, Problem, StructuredNote
from apps.api.services.fhir_mapper import build_fhir_bundle


def test_fhir_bundle_structure():
    note = StructuredNote(
        chief_complaint="cough",
        hpi="3 days",
        ros="no fever",
        assessment_plan="hydration",
        problems=[Problem(text="cough", confidence=0.9)],
    )
    encounter = EncounterInput.model_validate(
        {"start": datetime.utcnow(), "end": datetime.utcnow(), "class": "AMB", "reason": "cough"}
    )
    patient = PatientInput(id="p1")
    bundle = build_fhir_bundle(note, encounter, patient)

    assert bundle["resourceType"] == "Bundle"
    resources = [entry["resource"]["resourceType"] for entry in bundle["entry"]]
    assert "Encounter" in resources
    assert "Condition" in resources
    assert "Observation" in resources
