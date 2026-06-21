# SOC Platform Architecture

## Overview

The SOC Platform is a mini SIEM + SOAR backend built with FastAPI. It is designed to simulate a simplified security operations workflow:

- ingest raw security log lines
- normalize and parse event data
- evaluate events against detection rules
- group related alerts into incidents
- generate response actions for critical incidents

## Core Components

### app/main.py
Entry point for the FastAPI application. It initializes the API and includes routes.

### app/api/routes.py
Defines API routes for ingestion, health checks, alert listing, incident retrieval, and action triggering.

### app/core/parser.py
Converts raw log strings into structured `SecurityEvent` objects.

### app/detection
Contains rule-based detection logic:
- `BruteForceRule`
- `MalwareRule`
- `PortScanRule`
- `PowerShellAbuseRule`

### app/correlation/engine.py
Correlates related alerts into incidents using source IP and time-window logic.

### app/incident/manager.py
Provides a simple API for listing and retrieving incidents.

### app/soar/response.py
Generates response actions based on incident severity and alert type.

### app/storage/repository.py
In-memory repository for alerts and incidents, keeping the system lightweight.

## Deployment

### Docker
The project supports both local development and production-style Docker setups:

- `docker-compose.yml` — base service configuration.
- `docker-compose.override.yml` — mounts local source and enables Uvicorn reload for dev.
- `docker-compose.prod.yml` — production-style runtime without source mounts.

### Packaging
Package metadata is declared in `pyproject.toml`, enabling editable installs and proper dependency management.

## Test Coverage

The repository includes unit tests around:
- log parsing
- detection rules
- correlation engine
- API endpoints

## Why this project is portfolio-worthy

- Demonstrates backend design with modular service responsibility.
- Uses modern Python packaging and Docker deployment.
- Includes testable architecture and CI validation.
- Shows practical security automation use cases.
