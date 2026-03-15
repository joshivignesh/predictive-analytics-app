"""Dataset API endpoints.

Supports:
  GET  /datasets         — list all uploaded datasets
  POST /datasets         — upload a new CSV/JSON file
  GET  /datasets/{id}    — get dataset detail
  DELETE /datasets/{id}  — remove a dataset
"""
import uuid

import structlog
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.dataset import DatasetCreate, DatasetResponse, DatasetSummary
from app.services.dataset_service import DatasetService

log = structlog.get_logger(__name__)
router = APIRouter()

_ALLOWED_CONTENT_TYPES = {
    "text/csv",
    "application/json",
    "application/octet-stream",
}


@router.get(
    "/",
    response_model=list[DatasetSummary],
    summary="List all datasets",
)
async def list_datasets(
    db: AsyncSession = Depends(get_db),
) -> list[DatasetSummary]:
    svc = DatasetService(db)
    datasets = await svc.list_datasets()
    return [DatasetSummary.model_validate(d) for d in datasets]


@router.post(
    "/",
    response_model=DatasetResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a dataset file",
)
async def upload_dataset(
    name: str,
    file: UploadFile = File(..., description="CSV or JSON dataset file"),
    description: str | None = None,
    target_column: str | None = None,
    db: AsyncSession = Depends(get_db),
) -> DatasetResponse:
    if file.content_type and file.content_type not in _ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type: {file.content_type}. Upload CSV or JSON.",
        )

    svc = DatasetService(db)
    meta = DatasetCreate(name=name, description=description, target_column=target_column)
    dataset = await svc.create_from_upload(meta, file)
    return DatasetResponse.model_validate(dataset)


@router.get(
    "/{dataset_id}",
    response_model=DatasetResponse,
    summary="Get dataset by ID",
)
async def get_dataset(
    dataset_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> DatasetResponse:
    svc = DatasetService(db)
    dataset = await svc.get_by_id(dataset_id)
    if dataset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")
    return DatasetResponse.model_validate(dataset)


@router.delete(
    "/{dataset_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a dataset",
)
async def delete_dataset(
    dataset_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    svc = DatasetService(db)
    deleted = await svc.delete(dataset_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")
