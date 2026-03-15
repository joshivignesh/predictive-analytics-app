"""Health check endpoints.

Two standard endpoints used by Kubernetes / Docker Compose:
  GET /health/live   — process is alive
  GET /health/ready  — service can handle requests (DB reachable, etc.)
"""
import structlog
from fastapi import APIRouter
from pydantic import BaseModel

from app.core.config import settings

log = structlog.get_logger(__name__)
router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str


@router.get(
    "/live",
    response_model=HealthResponse,
    summary="Liveness probe",
    description="Returns 200 if the process is running. Used by Kubernetes liveness probes.",
)
async def liveness() -> HealthResponse:
    return HealthResponse(
        status="ok",
        version=settings.APP_VERSION,
        environment=settings.ENV,
    )


@router.get(
    "/ready",
    response_model=HealthResponse,
    summary="Readiness probe",
    description="Returns 200 when the service is ready to serve traffic.",
)
async def readiness() -> HealthResponse:
    log.info("readiness_check", status="ok")
    return HealthResponse(
        status="ok",
        version=settings.APP_VERSION,
        environment=settings.ENV,
    )
