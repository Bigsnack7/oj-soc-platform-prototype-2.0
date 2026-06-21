from abc import ABC, abstractmethod
from typing import Any

from app.core.models import Alert, SecurityEvent, Severity


class BaseRule(ABC):
    """Base interface for all detection rules."""

    name: str = "BASE_RULE"
    severity: Severity = "LOW"
    description: str = ""
    mitre_technique: str = ""

    @abstractmethod
    def evaluate(self, event: SecurityEvent) -> Alert | None:
        """Return an Alert when the event matches the rule."""
        raise NotImplementedError

    def build_alert(self, event: SecurityEvent, rule_name: str | None = None) -> Alert:
        return Alert(
            rule=rule_name or self.name,
            severity=self.severity,
            description=self.description,
            event=event,
            mitre_technique=self.mitre_technique,
        )
