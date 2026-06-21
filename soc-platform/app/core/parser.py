import re
from datetime import datetime, timezone
from typing import Optional

from .models import SecurityEvent


LOG_PATTERN = re.compile(
    r"""
    ^
    (?P<timestamp>\S+)
    \s+-\s+SOURCE:\s*(?P<source>[^-]+?)
    \s+-\s+IP:\s*(?P<ip>[\d.:a-fA-F]+)
    \s+-\s+MSG:\s*(?P<message>.*)
    $
    """,
    re.VERBOSE,
)


def _normalize_timestamp(timestamp: str) -> Optional[str]:
    """Normalize an ISO-8601 timestamp and enforce timezone awareness."""

    if timestamp.endswith("Z"):
        timestamp = timestamp[:-1] + "+00:00"

    try:
        parsed = datetime.fromisoformat(timestamp)
    except ValueError:
        return None

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)

    return parsed.isoformat()


def parse_log(raw: str) -> Optional[SecurityEvent]:
    """Convert a raw log line into a normalized SecurityEvent.

    Expected format:
        2026-06-20T20:15:01Z - SOURCE: WindowsAuth - IP: 10.0.0.52 - MSG: Failed login attempt
    """

    raw = raw.strip()
    match = LOG_PATTERN.fullmatch(raw)
    if not match:
        return None

    data = match.groupdict()
    timestamp = _normalize_timestamp(data["timestamp"].strip())
    if timestamp is None:
        return None

    return SecurityEvent(
        timestamp=timestamp,
        source=data["source"].strip(),
        ip=data["ip"].strip(),
        message=data["message"].strip(),
        raw=raw,
    )
