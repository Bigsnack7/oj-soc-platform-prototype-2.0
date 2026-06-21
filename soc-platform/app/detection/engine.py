from __future__ import annotations

from typing import Iterable, List, Type

from app.core.models import Alert, SecurityEvent
from .base import BaseRule
from .rules import (
    BruteForceRule,
    MalwareRule,
    PortScanRule,
    PowerShellAbuseRule,
)

DEFAULT_RULE_CLASSES: tuple[Type[BaseRule], ...] = (
    BruteForceRule,
    MalwareRule,
    PortScanRule,
    PowerShellAbuseRule,
)


class DetectionEngine:
    """Runs an event through the configured detection rules."""

    def __init__(self, rules: Iterable[BaseRule] | None = None) -> None:
        self.rules = list(rules) if rules is not None else [cls() for cls in DEFAULT_RULE_CLASSES]

    def run(self, event: SecurityEvent) -> List[Alert]:
        return [
            alert
            for rule in self.rules
            if (alert := rule.evaluate(event)) is not None
        ]


# Shared engine instance for the application.
detection_engine = DetectionEngine()
