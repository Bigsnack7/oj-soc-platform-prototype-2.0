from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from app.core.models import Alert, Incident


@dataclass(slots=True)
class InMemoryRepository:
    """Simple repository for alerts and incidents.

    The repository abstraction keeps the application structure professional and
    allows the storage layer to be replaced later with PostgreSQL, Redis, or
    OpenSearch without changing the rest of the app.
    """

    alerts: List[Alert] = field(default_factory=list)
    incidents: Dict[str, Incident] = field(default_factory=dict)

    def add_alert(self, alert: Alert) -> None:
        self.alerts.append(alert)

    def list_alerts(self) -> List[Alert]:
        return list(self.alerts)

    def add_incident(self, incident: Incident) -> None:
        self.incidents[incident.incident_id] = incident

    def list_incidents(self) -> List[Incident]:
        return list(self.incidents.values())

    def get_incident(self, incident_id: str) -> Optional[Incident]:
        return self.incidents.get(incident_id)

    def clear_alerts(self) -> None:
        """Clear stored alerts."""
        self.alerts.clear()

    def clear_incidents(self) -> None:
        """Clear stored incidents."""
        self.incidents.clear()

    def clear(self) -> None:
        """Clear all stored repository state."""
        self.clear_alerts()
        self.clear_incidents()


repository = InMemoryRepository()
