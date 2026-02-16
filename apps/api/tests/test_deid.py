from apps.api.services.deid import Deidentifier


def test_deid_redacts_phi():
    text = "John Doe MRN 12345678 lives at 1 Main St on 01/02/2026 email john@example.com phone 555-123-4567"
    redacted, entities = Deidentifier().deidentify(text)

    assert "john@example.com" not in redacted.lower()
    assert "12345678" not in redacted
    assert "[EMAIL]" in redacted
    assert "[MRN]" in redacted
    assert len(entities) >= 2
