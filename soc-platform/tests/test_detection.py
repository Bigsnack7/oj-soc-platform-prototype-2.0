import pytest

from app.core.models import SecurityEvent
from app.core.state import failed_login_tracker
from app.detection.engine import DetectionEngine


@pytest.fixture(autouse=True)
def reset_failed_login_tracker() -> None:
    failed_login_tracker.clear()


def test_brute_force_detection():
    engine = DetectionEngine()

    ip = "10.0.0.9"
    event1 = SecurityEvent(timestamp="t1", source="auth", ip=ip, message="Failed login attempt")
    event2 = SecurityEvent(timestamp="t2", source="auth", ip=ip, message="Failed login attempt")
    event3 = SecurityEvent(timestamp="t3", source="auth", ip=ip, message="Failed login attempt")

    assert engine.run(event1) == []
    assert engine.run(event2) == []

    alerts = engine.run(event3)
    assert len(alerts) == 1
    assert alerts[0].rule == "BRUTE_FORCE"
    assert alerts[0].severity == "MEDIUM"
    assert "failed login" in alerts[0].description.lower()


def test_malware_detection():
    engine = DetectionEngine()

    event = SecurityEvent(
        timestamp="t",
        source="endpoint",
        ip="10.0.0.10",
        message="Mimikatz execution detected",
    )

    alerts = engine.run(event)
    assert len(alerts) == 1
    assert alerts[0].rule == "MALWARE"
    assert alerts[0].severity == "CRITICAL"
