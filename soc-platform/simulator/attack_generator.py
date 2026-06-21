from __future__ import annotations

import argparse
import logging
from typing import Iterable

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

SAMPLE_LOGS = [
    "2026-06-20T20:15:01Z - SOURCE: WindowsAuth - IP: 10.0.0.52 - MSG: Failed login attempt",
    "2026-06-20T20:15:02Z - SOURCE: WindowsAuth - IP: 10.0.0.52 - MSG: Failed login attempt",
    "2026-06-20T20:15:03Z - SOURCE: WindowsAuth - IP: 10.0.0.52 - MSG: Failed login attempt",
    "2026-06-20T20:15:04Z - SOURCE: Endpoint - IP: 10.0.0.52 - MSG: mimikatz execution detected",
]


logger = logging.getLogger("simulator.attack_generator")
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)


def send_logs(api_url: str, logs: Iterable[str], timeout: int = 10) -> None:
    """Send log lines to the API endpoint."""
    session = requests.Session()
    retries = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["POST"],
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    for raw_log in logs:
        payload = {"raw_log": raw_log}
        logger.info("Sending log: %s", raw_log)

        try:
            response = session.post(api_url, json=payload, timeout=timeout)
            response.raise_for_status()
            logger.info("Response: %s", response.json())
        except requests.RequestException as exc:
            logger.error("Failed sending log: %s", exc)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send simulated attack logs to the SOC API.")
    parser.add_argument(
        "--api-url",
        default="http://localhost:8000/event",
        help="Target event ingestion endpoint.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Request timeout in seconds.",
    )
    parser.add_argument(
        "--logs",
        nargs="*",
        default=SAMPLE_LOGS,
        help="Custom log lines to send. If omitted, sample logs are used.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    send_logs(args.api_url, args.logs, timeout=args.timeout)


if __name__ == "__main__":
    main()
