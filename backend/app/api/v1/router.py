"""Top-level v1 API router.

Each domain (health, datasets, models, predictions) has its own module.
Add new routers here as the project grows.
"""
from fastapi import APIRouter

from app.api.v1.endpoints import health

api_router = APIRouter()

api_router.include_router(
    health.router,
    prefix="/health",
    tags=["health"],
)
