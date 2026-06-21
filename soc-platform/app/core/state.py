from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from threading import Lock
from typing import DefaultDict, List

from .models import Alert


failed_login_tracker: DefaultDict[str, int] = defaultdict(int)


@dataclass(slots=True)
class CorrelationState:
    """Shared in-memory state used by the correlation engine.

    The project keeps this lightweight and easy to understand, but the class is
    intentionally isolated so it can later be replaced with Redis or a database.
    """

    alert_buffer: DefaultDict[str, List[Alert]] = field(
        default_factory=lambda: defaultdict(list)
    )
    lock: Lock = field(default_factory=Lock)

    def add_alert(self, ip: str, alert: Alert) -> None:
        with self.lock:
            self.alert_buffer[ip].append(alert)

    def get_alerts(self, ip: str) -> List[Alert]:
        return list(self.alert_buffer[ip])

    def clear_alerts(self, ip: str) -> None:
        with self.lock:
            self.alert_buffer[ip] = []

    def clear(self) -> None:
        with self.lock:
            self.alert_buffer.clear()


correlation_state = CorrelationState()
