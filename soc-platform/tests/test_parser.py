from datetime import datetime, timezone

from app.core.parser import parse_log


def test_parse_log_success():
    raw = "2026-06-20T20:15:01Z - SOURCE: WindowsAuth - IP: 10.0.0.52 - MSG: Failed login attempt"
    event = parse_log(raw)

    assert event is not None
    assert event.source == "WindowsAuth"
    assert event.ip == "10.0.0.52"
    assert event.message == "Failed login attempt"
    assert event.raw == raw
    assert event.timestamp.endswith("+00:00")
    assert datetime.fromisoformat(event.timestamp).tzinfo is not None


def test_parse_log_invalid_format():
    assert parse_log("not-a-valid-log") is None
