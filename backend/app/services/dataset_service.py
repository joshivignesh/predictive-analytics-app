"""Dataset service layer.

All business logic for datasets lives here, keeping the API
route handlers thin and focused on HTTP concerns only.
"""
import io
import uuid
from pathlib import Path

import pandas as pd
import structlog
from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.dataset import Dataset
from app.schemas.dataset import DatasetCreate

log = structlog.get_logger(__name__)


class DatasetService:
    """CRUD operations and file handling for datasets."""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def list_datasets(self) -> list[Dataset]:
        result = await self._db.execute(select(Dataset).order_by(Dataset.created_at.desc()))
        return list(result.scalars().all())

    async def get_by_id(self, dataset_id: uuid.UUID) -> Dataset | None:
        return await self._db.get(Dataset, dataset_id)

    async def create_from_upload(
        self,
        meta: DatasetCreate,
        file: UploadFile,
    ) -> Dataset:
        """Persist dataset metadata and infer column info from the uploaded file."""
        raw = await file.read()
        file_size = len(raw)

        # Parse to infer schema — support CSV and JSON
        row_count: int | None = None
        column_count: int | None = None
        column_names: str | None = None

        try:
            suffix = Path(file.filename or "").suffix.lower()
            if suffix == ".csv":
                df = pd.read_csv(io.BytesIO(raw))
            elif suffix in (".json", ".jsonl"):
                df = pd.read_json(io.BytesIO(raw))
            else:
                df = pd.read_csv(io.BytesIO(raw))  # Best-effort fallback

            row_count = len(df)
            column_count = len(df.columns)
            column_names = ",".join(df.columns.tolist())
        except Exception as exc:
            log.warning("dataset_parse_failed", filename=file.filename, error=str(exc))

        # Save file to disk under MODELS_DIR/datasets/
        upload_dir = Path(settings.MODELS_DIR) / "datasets"
        upload_dir.mkdir(parents=True, exist_ok=True)
        saved_filename = f"{uuid.uuid4()}_{file.filename}"
        (upload_dir / saved_filename).write_bytes(raw)

        dataset = Dataset(
            name=meta.name,
            description=meta.description,
            filename=saved_filename,
            file_size_bytes=file_size,
            row_count=row_count,
            column_count=column_count,
            columns=column_names,
            target_column=meta.target_column,
        )
        self._db.add(dataset)
        await self._db.flush()  # Populate id before returning

        log.info(
            "dataset_created",
            dataset_id=str(dataset.id),
            name=dataset.name,
            rows=row_count,
            columns=column_count,
        )
        return dataset

    async def delete(self, dataset_id: uuid.UUID) -> bool:
        dataset = await self.get_by_id(dataset_id)
        if dataset is None:
            return False
        await self._db.delete(dataset)
        return True
