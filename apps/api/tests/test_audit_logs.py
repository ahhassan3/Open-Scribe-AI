import logging

from fastapi.testclient import TestClient

from apps.api.main import app


def test_audit_logs_phi_safe_and_correlation_id(caplog):
    client = TestClient(app)
    caplog.set_level(logging.INFO)
    payload = {
        "text": "Jane Doe MRN 777888 email jane@example.com",
    }
    response = client.post("/v1/ingest/deidentify", json=payload, headers={"X-Correlation-ID": "corr-1"})

    assert response.status_code == 200
    assert response.json()["correlation_id"] == "corr-1"

    log_text = "\n".join(record.message for record in caplog.records)
    assert "jane@example.com" not in log_text.lower()
    assert "777888" not in log_text
    assert any(getattr(record, "correlation_id", None) == "corr-1" for record in caplog.records)
    assert any(getattr(record, "event_name", None) in {"ingest_deidentify", "request_completed"} for record in caplog.records)
