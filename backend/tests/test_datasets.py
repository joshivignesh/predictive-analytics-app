"""Unit tests for the dataset service.

Uses an in-memory SQLite database so tests run without a real Postgres
instance — swap asyncpg URL for aiosqlite in test fixtures.
"""
import io
import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.schemas.dataset import DatasetCreate


@pytest.mark.asyncio
async def test_dataset_create_schema_validation() -> None:
    """DatasetCreate must reject empty names."""
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        DatasetCreate(name="")  # min_length=1


@pytest.mark.asyncio
async def test_dataset_create_schema_valid() -> None:
    meta = DatasetCreate(
        name="House Prices",
        description="Boston dataset",
        target_column="price",
    )
    assert meta.name == "House Prices"
    assert meta.target_column == "price"
