from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "SOC Platform"
    assert body["status"] == "running"


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "soc-platform"}


def test_ingest_event_invalid_format():
    response = client.post("/event", json={"raw_log": "bad log line"})
    assert response.status_code == 400


def test_ingest_event_success():
    payload = {
        "raw_log": "2026-06-20T20:15:01Z - SOURCE: WindowsAuth - IP: 10.0.0.52 - MSG: Failed login attempt"
    }
    response = client.post("/event", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["parsed"] is True
    assert isinstance(body["alerts"], list)
    assert body["incidents_created"] == 0
