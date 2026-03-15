"""Top-level v1 API router."""
from fastapi import APIRouter

from app.api.v1.endpoints import datasets, health

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(datasets.router, prefix="/datasets", tags=["datasets"])
