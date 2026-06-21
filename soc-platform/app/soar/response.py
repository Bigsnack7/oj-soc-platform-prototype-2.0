from __future__ import annotations

from typing import List

from app.core.models import Incident

HIGH_SEVERITIES = frozenset({"HIGH", "CRITICAL"})
RULE_ACTIONS = {
    "MALWARE": "Isolate endpoint for investigation",
    "BRUTE_FORCE_SUCCESS": "Force password reset and review authentication logs",
}


class SOAREngine:
    """Very small response automation layer.

    The goal is not to actually block systems, but to demonstrate how detection
    can feed response actions in a SOC workflow.
    """

    def execute(self, incident: Incident) -> List[str]:
        actions: List[str] = []
        alert_rules = {alert.rule for alert in incident.alerts}

        if incident.severity in HIGH_SEVERITIES:
            actions.append(f"Block source IP: {incident.ip}")

        for rule, action in RULE_ACTIONS.items():
            if rule in alert_rules:
                actions.append(action)

        return actions


soar_engine = SOAREngine()
