"""Dataset ORM model.

Represents a user-uploaded CSV/JSON dataset stored in the system.
The actual file bytes are stored on disk (or object storage in prod);
this table holds the metadata.
"""
from sqlalchemy import BigInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class Dataset(TimestampMixin, Base):
    """Metadata for an uploaded dataset file."""

    __tablename__ = "datasets"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    filename: Mapped[str] = mapped_column(String(512), nullable=False)
    file_size_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False)
    row_count: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    column_count: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    # Comma-separated list of column names (stored flat for simplicity)
    columns: Mapped[str | None] = mapped_column(Text, nullable=True)
    target_column: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Relationships
    ml_models: Mapped[list["MLModel"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        back_populates="dataset",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Dataset id={self.id} name={self.name!r}>"
