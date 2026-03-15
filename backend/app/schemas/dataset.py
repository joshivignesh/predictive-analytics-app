"""Pydantic schemas for the Dataset domain.

Separate schemas for:
  - DatasetCreate   — input validation on upload
  - DatasetSummary  — lightweight list item
  - DatasetResponse — full detail with all fields
"""
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DatasetCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, examples=["House Prices 2024"])
    description: str | None = Field(None, max_length=2000)
    target_column: str | None = Field(None, max_length=255, examples=["price"])


class DatasetSummary(BaseModel):
    """Lightweight payload for list endpoints."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    filename: str
    file_size_bytes: int
    row_count: int | None
    column_count: int | None
    created_at: datetime


class DatasetResponse(DatasetSummary):
    """Full detail payload."""

    description: str | None
    columns: str | None
    target_column: str | None
    updated_at: datetime
