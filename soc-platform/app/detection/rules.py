from app.core.models import Alert, SecurityEvent
from app.core.state import failed_login_tracker
from .base import BaseRule


class BruteForceRule(BaseRule):
    """Detect repeated failed logins from the same source IP."""

    name = "BRUTE_FORCE"
    severity = "MEDIUM"
    description = "Multiple failed login attempts detected"
    mitre_technique = "T1110"

    def evaluate(self, event: SecurityEvent) -> Alert | None:
        message = event.message.lower()

        if "failed login" in message:
            failed_login_tracker[event.ip] += 1

            if failed_login_tracker[event.ip] >= 3:
                return self.build_alert(event)

        if "successful login" in message:
            if failed_login_tracker[event.ip] >= 3:
                alert = Alert(
                    rule="BRUTE_FORCE_SUCCESS",
                    severity="CRITICAL",
                    description="Successful login after repeated failed attempts",
                    event=event,
                    mitre_technique=self.mitre_technique,
                )
                failed_login_tracker[event.ip] = 0
                return alert

            failed_login_tracker[event.ip] = 0

        return None


class MalwareRule(BaseRule):
    """Detect suspicious malware-related indicators."""

    name = "MALWARE"
    severity = "CRITICAL"
    description = "Credential dumping or malware tooling detected"
    mitre_technique = "T1003"

    def evaluate(self, event: SecurityEvent) -> Alert | None:
        message = event.message.lower()

        indicators = ("mimikatz", "lsass dump", "credential dumping")
        if any(indicator in message for indicator in indicators):
            return self.build_alert(event)
        return None


class PortScanRule(BaseRule):
    """Detect likely port-scanning activity."""

    name = "PORT_SCAN"
    severity = "HIGH"
    description = "Potential port scanning behavior detected"
    mitre_technique = "T1046"

    def evaluate(self, event: SecurityEvent) -> Alert | None:
        message = event.message.lower()
        if "port scan" in message or "nmap" in message:
            return self.build_alert(event)
        return None


class PowerShellAbuseRule(BaseRule):
    """Detect suspicious PowerShell execution patterns."""

    name = "POWERSHELL_ABUSE"
    severity = "HIGH"
    description = "Suspicious PowerShell activity detected"
    mitre_technique = "T1059.001"

    def evaluate(self, event: SecurityEvent) -> Alert | None:
        message = event.message.lower()
        if "powershell" in message and ("-enc" in message or "encodedcommand" in message):
            return self.build_alert(event)
        return None
