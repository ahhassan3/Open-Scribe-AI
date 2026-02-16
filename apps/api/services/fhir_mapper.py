from apps.api.models.schemas import EncounterInput, PatientInput, StructuredNote


def build_fhir_bundle(note: StructuredNote, encounter: EncounterInput, patient: PatientInput) -> dict:
    entries = [
        {
            "resource": {
                "resourceType": "Encounter",
                "status": "finished",
                "class": {"code": encounter.class_code},
                "subject": {"reference": f"Patient/{patient.id}"},
                "period": {"start": encounter.start.isoformat(), "end": encounter.end.isoformat()},
                "reasonCode": [{"text": encounter.reason}],
            }
        }
    ]

    for problem in note.problems:
        entries.append(
            {
                "resource": {
                    "resourceType": "Condition",
                    "clinicalStatus": {"coding": [{"code": "active"}]},
                    "code": {"text": problem.text},
                    "subject": {"reference": f"Patient/{patient.id}"},
                }
            }
        )

    if note.ros:
        entries.append(
            {
                "resource": {
                    "resourceType": "Observation",
                    "status": "final",
                    "code": {"text": "Review of Systems"},
                    "subject": {"reference": f"Patient/{patient.id}"},
                    "valueString": note.ros,
                }
            }
        )

    entries.append(
        {
            "resource": {
                "resourceType": "DocumentReference",
                "status": "current",
                "subject": {"reference": f"Patient/{patient.id}"},
                "description": "Structured clinical note",
                "content": [{"attachment": {"contentType": "application/json", "title": "note"}}],
            }
        }
    )

    return {"resourceType": "Bundle", "type": "collection", "entry": entries}
