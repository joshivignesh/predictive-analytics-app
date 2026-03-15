"""MLModel ORM model.

Represents a trained machine learning model artefact.
Each model belongs to a dataset and records its training metrics.
"""
import uuid

from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class MLModel(TimestampMixin, Base):
    """A trained predictive model and its evaluation metrics."""

    __tablename__ = "ml_models"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    algorithm: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Path to the serialised model file (relative to MODELS_DIR)
    artefact_path: Mapped[str | None] = mapped_column(String(512), nullable=True)

    # Training metrics (nullable until training completes)
    accuracy: Mapped[float | None] = mapped_column(Float, nullable=True)
    precision: Mapped[float | None] = mapped_column(Float, nullable=True)
    recall: Mapped[float | None] = mapped_column(Float, nullable=True)
    f1_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    r2_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    rmse: Mapped[float | None] = mapped_column(Float, nullable=True)

    # MLflow run ID for experiment tracking
    mlflow_run_id: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # FK to the dataset used for training
    dataset_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("datasets.id", ondelete="CASCADE"),
        nullable=False,
    )
    dataset: Mapped["Dataset"] = relationship(back_populates="ml_models")  # type: ignore[name-defined]  # noqa: F821

    # Predictions made using this model
    predictions: Mapped[list["Prediction"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        back_populates="model",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<MLModel id={self.id} name={self.name!r} algo={self.algorithm!r}>"
