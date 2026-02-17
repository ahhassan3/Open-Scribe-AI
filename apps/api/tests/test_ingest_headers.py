from fastapi.testclient import TestClient

from apps.api.main import app


def test_ingest_rejects_malformed_content_length_header():
    client = TestClient(app)
    response = client.post(
        "/v1/ingest/audio",
        content=b"",
        headers={"Content-Length": "abc", "Content-Type": "multipart/form-data; boundary=boundary"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid Content-Length header"
