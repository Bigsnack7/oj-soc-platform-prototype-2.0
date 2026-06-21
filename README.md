# SOC Platform

A polished portfolio project demonstrating a professional **Python backend** for security operations automation.

This mini SIEM + SOAR platform is designed for recruiters to review real backend engineering skills, including:
- Docker deployment and package metadata
- FastAPI API design and request validation
- modular detection, correlation, incident management, and SOAR response flows
- testable architecture with unit tests and CI
- proprietary-ready licensing for private portfolio work

## Portfolio Highlights

- **FastAPI** backend with a clear service boundary and route definitions.
- **Modular architecture** separating ingestion, detection, correlation, incident handling, and automated responses.
- **Docker-ready** development and production flows with `docker-compose` overrides.
- **Package metadata** defined in `pyproject.toml` for modern Python packaging.
- **CI workflow** validates the package install path and runs tests on push.

## Features

- Log ingestion API for raw security event input
- Structured parser for normalized event creation
- Rule-based alert generation for brute force, malware, port scan, and PowerShell abuse
- Correlation engine that groups alerts into incidents
- In-memory repository abstraction for alerts and incidents
- SOAR response engine with actionable remediation recommendations
- Simulator for sending sample attack logs
- Docker development and production-ready configuration
- Editable package install and test dependencies

## Tech stack

- Python 3.14
- FastAPI
- Uvicorn
- Pydantic
- Docker Compose
- GitHub Actions

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for a detailed component and deployment overview.

## Project Structure

```text
soc-platform/
├── app/
│   ├── main.py
│   ├── api/
│   ├── core/
│   ├── correlation/
│   ├── detection/
│   ├── incident/
│   ├── soar/
│   └── storage/
├── simulator/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── docker-compose.override.yml
├── docker-compose.prod.yml
├── pyproject.toml
├── requirements.txt
└── README.md
```

## How It Works

1. A client submits a raw log line to the ingestion endpoint.
2. The parser normalizes the log into a structured security event.
3. Detection rules evaluate the event and emit alerts.
4. Alerts are stored in an in-memory repository.
5. The correlation engine groups related alerts and creates incidents.
6. The SOAR engine generates response actions for high-risk incidents.

## Example Log Format

```text
2026-06-20T20:15:01Z - SOURCE: WindowsAuth - IP: 10.0.0.52 - MSG: Failed login attempt
```

## Quick Start

### Local

```bash
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Or install the package in editable mode with test dependencies:

```bash
python -m pip install -e .[test]
cp .env.example .env
uvicorn app.main:app --reload
```

Open the API docs:

```bash
http://localhost:8000/docs
```

### Docker

```bash
cp .env.example .env
docker compose up --build
```

This uses the local development override defined in `docker-compose.override.yml`.

For a production-style run:

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build
```

## API Endpoints

### `GET /`
Returns service status.

### `GET /health`
Health check endpoint.

### `POST /event`
Ingest a raw log line.

Example body:

```json
{
  "raw_log": "2026-06-20T20:15:01Z - SOURCE: WindowsAuth - IP: 10.0.0.52 - MSG: Failed login attempt"
}
```

### `GET /alerts`
Lists stored alerts.

### `GET /incidents`
Lists stored incidents.

### `GET /incidents/{incident_id}`
Returns one incident.

### `POST /actions/{incident_id}`
Triggers SOAR actions for an incident.

## Simulator

Send sample attack logs to the running API:

```bash
python simulator/attack_generator.py
```

## Tests

```bash
pytest -q
```

If you want to run a single file:

```bash
pytest tests/test_api.py -q
```

## Future Improvements

This repository is intentionally lightweight and easy to understand. A natural next step would be:
- PostgreSQL for durable storage
- Redis for state and caching
- Kafka for streaming ingestion
- OpenSearch for searchable event storage
- React dashboard for analyst workflows
- authentication and authorization for API access

## License

This project is proprietary software. All rights are reserved by the copyright owner.
Unauthorized reuse, distribution, or derivative work is prohibited unless you have
explicit written permission.
