from fastapi import FastAPI

from app.api.routes import router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Mini SIEM + SOAR platform for log ingestion, detection, correlation, and response.",
)

app.include_router(router)


@app.get("/")
def root() -> dict[str, str]:
    """A minimal landing endpoint for quick smoke tests."""

    return {
        "service": settings.app_name,
        "status": "running",
        "docs": "/docs",
    }
