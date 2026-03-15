"""Pydantic schemas for the MLModel domain."""
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MLModelSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    algorithm: str
    dataset_id: uuid.UUID
    accuracy: float | None
    f1_score: float | None
    created_at: datetime


class MLModelResponse(MLModelSummary):
    description: str | None
    precision: float | None
    recall: float | None
    r2_score: float | None
    rmse: float | None
    mlflow_run_id: str | None
    artefact_path: str | None
    updated_at: datetime
