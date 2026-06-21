from app.core.models import Alert, SecurityEvent
from app.core.state import correlation_state
from app.correlation.engine import CorrelationEngine
from app.storage.repository import repository


def test_correlation_creates_incident():
    repository.clear()
    correlation_state.clear()

    engine = CorrelationEngine(min_alerts=2)

    event = SecurityEvent(timestamp="t", source="auth", ip="10.0.0.55", message="Failed login attempt")
    alert1 = Alert(rule="BRUTE_FORCE", severity="MEDIUM", description="Failed login attempts", event=event)
    alert2 = Alert(rule="MALWARE", severity="CRITICAL", description="Malware detected", event=event)

    assert engine.correlate(alert1) is None

    incident = engine.correlate(alert2)
    assert incident is not None
    assert incident.ip == "10.0.0.55"
    assert incident.severity == "CRITICAL"
    assert repository.get_incident(incident.incident_id) is not None
    assert correlation_state.get_alerts("10.0.0.55") == []
