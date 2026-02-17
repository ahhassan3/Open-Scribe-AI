from types import SimpleNamespace

from apps.api.services.deid import Deidentifier


def test_deid_redacts_phi():
    text = "John Doe MRN 12345678 lives at 1 Main St on 01/02/2026 email john@example.com phone 555-123-4567"
    redacted, entities = Deidentifier().deidentify(text)

    assert "john@example.com" not in redacted.lower()
    assert "12345678" not in redacted
    assert "[EMAIL]" in redacted
    assert "MRN" not in redacted
    assert len(entities) >= 2


def test_analyzer_findings_are_applied_to_output():
    svc = Deidentifier()

    class FakeAnalyzer:
        def analyze(self, text: str, entities, language: str):
            start = text.index("Boston")
            end = start + len("Boston")
            return [SimpleNamespace(start=start, end=end, entity_type="LOCATION")]

    svc.analyzer = FakeAnalyzer()
    redacted, entities = svc.deidentify("Patient lives in Boston and has cough")

    assert "Boston" not in redacted
    assert "[LOCATION]" in redacted
    assert any(e["entity_type"] == "LOCATION" for e in entities)
