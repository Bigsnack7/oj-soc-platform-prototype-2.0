from __future__ import annotations

from typing import List, Optional

from app.core.models import Incident
from app.storage.repository import repository


class IncidentManager:
    """Provides a clean interface for working with incidents."""

    def list_incidents(self) -> List[Incident]:
        return repository.list_incidents()

    def get_incident(self, incident_id: str) -> Optional[Incident]:
        return repository.get_incident(incident_id)


incident_manager = IncidentManager()
