from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import List, Optional
from uuid import uuid4

from app.core.models import Alert, Incident
from app.core.state import correlation_state
from app.storage.repository import repository


class CorrelationEngine:
    """Groups related alerts into incidents.

    This implementation keeps the logic easy to follow:
    - alerts are grouped by source IP
    - if multiple alerts arrive close together, an incident is created
    - severity is escalated based on the collected alerts

    In a real environment, this would be backed by a queue or stream processor.
    """

    def __init__(self, window_minutes: int = 30, min_alerts: int = 2) -> None:
        self.window_minutes = window_minutes
        self.min_alerts = min_alerts

    def _is_recent(self, created_at: str) -> bool:
        try:
            alert_time = datetime.fromisoformat(created_at)
        except ValueError:
            # If the timestamp cannot be parsed, keep the system forgiving and
            # treat the alert as recent enough to be considered.
            return True

        now = datetime.now(timezone.utc)
        if alert_time.tzinfo is None:
            alert_time = alert_time.replace(tzinfo=timezone.utc)

        return now - alert_time <= timedelta(minutes=self.window_minutes)

    def correlate(self, alert: Alert) -> Optional[Incident]:
        ip = alert.event.ip

        with correlation_state.lock:
            buffer_for_ip = correlation_state.alert_buffer[ip]
            buffer_for_ip.append(alert)

            # Remove stale alerts from the correlation window.
            buffer_for_ip[:] = [
                item for item in buffer_for_ip if self._is_recent(item.created_at)
            ]

            if len(buffer_for_ip) < self.min_alerts:
                return None

            severity_order = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}
            highest_severity = max(
                buffer_for_ip,
                key=lambda item: severity_order.get(item.severity.upper(), 1),
            ).severity.upper()

            incident_id = f"INC-{uuid4().hex[:8]}"
            incident = Incident(
                incident_id=incident_id,
                ip=ip,
                alerts=list(buffer_for_ip),
                severity=highest_severity,
            )

            repository.add_incident(incident)
            correlation_state.clear_alerts(ip)

            return incident


correlation_engine = CorrelationEngine()
