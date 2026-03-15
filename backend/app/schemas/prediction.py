"""Pydantic schemas for prediction requests and responses."""
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PredictionRequest(BaseModel):
    model_id: uuid.UUID
    features: dict[str, float | int | str] = Field(
        ...,
        examples=[{"area_sqft": 1500, "bedrooms": 3, "location": "downtown"}],
    )


class PredictionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    model_id: uuid.UUID
    predicted_value: str
    confidence: float | None
    created_at: datetime
