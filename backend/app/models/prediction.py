"""Prediction ORM model.

Each row records a single inference request: the input features,
the predicted output, and the model confidence (if applicable).
"""
import uuid

from sqlalchemy import Float, ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class Prediction(TimestampMixin, Base):
    """Audit log of every prediction made by a model."""

    __tablename__ = "predictions"

    # Input features as JSON — flexible enough to handle any schema
    input_features: Mapped[dict] = mapped_column(JSONB, nullable=False)  # type: ignore[type-arg]

    # Predicted value (stored as text, cast at application layer)
    predicted_value: Mapped[str] = mapped_column(Text, nullable=False)

    # Confidence score in [0, 1] — None for regression models
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)

    # FK to the model that produced this prediction
    model_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("ml_models.id", ondelete="CASCADE"),
        nullable=False,
    )
    model: Mapped["MLModel"] = relationship(back_populates="predictions")  # type: ignore[name-defined]  # noqa: F821

    def __repr__(self) -> str:
        return (
            f"<Prediction id={self.id} "
            f"model_id={self.model_id} "
            f"predicted={self.predicted_value!r}>"
        )
