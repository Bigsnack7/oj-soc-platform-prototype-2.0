from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class EventRequest(BaseModel):
    """Incoming API payload carrying a raw log line."""

    raw_log: str = Field(..., min_length=1, description="Raw log line to ingest")


class AlertResponse(BaseModel):
    rule: str
    severity: str
    description: str
    ip: str
    created_at: str
    mitre_technique: str


class IncidentResponse(BaseModel):
    incident_id: str
    ip: str
    severity: str
    status: str
    created_at: str
    alert_rules: List[str]


class EventIngestResponse(BaseModel):
    parsed: bool
    alerts: List[AlertResponse] = Field(default_factory=list)
    incidents_created: int = 0
    actions: List[str] = Field(default_factory=list)


class HealthResponse(BaseModel):
    status: str
    service: str


class ErrorResponse(BaseModel):
    error: str


class IncidentActionResponse(BaseModel):
    incident_id: str
    actions: List[str]
    incident_found: bool
