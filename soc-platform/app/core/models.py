from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Literal


Severity = Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
IncidentStatus = Literal["OPEN", "CLOSED"]


def utc_now() -> str:
    """Return an ISO-8601 UTC timestamp."""

    return datetime.now(timezone.utc).isoformat()


@dataclass(slots=True, frozen=True)
class SecurityEvent:
    """Normalized security event used by the detection pipeline."""

    timestamp: str
    source: str
    ip: str
    message: str
    raw: str = ""


@dataclass(slots=True, frozen=True)
class Alert:
    """Detection output produced by a security rule."""

    rule: str
    severity: Severity
    description: str
    event: SecurityEvent
    created_at: str = field(default_factory=utc_now)
    mitre_technique: str = ""


@dataclass(slots=True)
class Incident:
    """Collection of related alerts that represent a single security incident."""

    incident_id: str
    ip: str
    alerts: List[Alert]
    severity: Severity
    status: IncidentStatus = "OPEN"
    created_at: str = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        self.status = self.status.upper()  # type: ignore[arg-type]
