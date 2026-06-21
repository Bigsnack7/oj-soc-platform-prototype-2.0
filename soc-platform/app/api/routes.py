from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from ..core.logger import logger
from ..core.models import Alert, Incident, SecurityEvent
from ..core.parser import parse_log
from ..detection.engine import detection_engine
from ..correlation.engine import correlation_engine
from ..incident.manager import incident_manager
from ..soar.response import soar_engine
from ..storage.repository import repository
from .schemas import (
    AlertResponse,
    ErrorResponse,
    EventIngestResponse,
    EventRequest,
    HealthResponse,
    IncidentActionResponse,
    IncidentResponse,
)

router = APIRouter()


def _alert_to_response(alert: Alert) -> AlertResponse:
    return AlertResponse(
        rule=alert.rule,
        severity=alert.severity,
        description=alert.description,
        ip=alert.event.ip,
        created_at=alert.created_at,
        mitre_technique=alert.mitre_technique,
    )


def _incident_to_response(incident: Incident) -> IncidentResponse:
    return IncidentResponse(
        incident_id=incident.incident_id,
        ip=incident.ip,
        severity=incident.severity,
        status=incident.status,
        created_at=incident.created_at,
        alert_rules=[alert.rule for alert in incident.alerts],
    )


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Simple health endpoint for GitHub and deployment checks."""

    return HealthResponse(status="ok", service="soc-platform")


@router.post(
    "/event",
    response_model=EventIngestResponse,
    responses={400: {"model": ErrorResponse}},
)
def ingest_event(payload: EventRequest) -> EventIngestResponse:
    """Ingest a raw log line, parse it, run detection, and correlate alerts."""

    event = parse_log(payload.raw_log)
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid log format. Expected: '<timestamp> - SOURCE: <source> - IP: <ip> - MSG: <message>'",
        )

    logger.info("Ingested event from %s (%s)", event.source, event.ip)

    alerts = detection_engine.run(event)
    for alert in alerts:
        repository.add_alert(alert)

    incidents_created = 0
    all_actions: list[str] = []

    for alert in alerts:
        incident = correlation_engine.correlate(alert)
        if incident is not None:
            incidents_created += 1
            all_actions.extend(soar_engine.execute(incident))

    return EventIngestResponse(
        parsed=True,
        alerts=[_alert_to_response(alert) for alert in alerts],
        incidents_created=incidents_created,
        actions=all_actions,
    )


@router.get("/alerts", response_model=list[AlertResponse])
def list_alerts() -> list[AlertResponse]:
    """Return all alerts currently stored in memory."""

    return [_alert_to_response(alert) for alert in repository.list_alerts()]


@router.get("/incidents", response_model=list[IncidentResponse])
def list_incidents() -> list[IncidentResponse]:
    """Return all incidents currently stored in memory."""

    return [_incident_to_response(incident) for incident in incident_manager.list_incidents()]


@router.get("/incidents/{incident_id}", response_model=IncidentResponse)
def get_incident(incident_id: str) -> IncidentResponse:
    incident = incident_manager.get_incident(incident_id)
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return _incident_to_response(incident)


@router.post("/actions/{incident_id}", response_model=IncidentActionResponse)
def trigger_actions(incident_id: str) -> IncidentActionResponse:
    """Manually trigger response actions for an existing incident."""

    incident = incident_manager.get_incident(incident_id)
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")

    actions = soar_engine.execute(incident)
    return IncidentActionResponse(
        incident_id=incident_id,
        actions=actions,
        incident_found=True,
    )
