"""Async SQLAlchemy engine and session factory.

We use the async flavour (asyncpg driver) throughout so that
FastAPI's async request handlers never block the event loop.
"""
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# Engine — connection pool shared across all requests
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.is_development,  # Log SQL in dev, silent in prod
    pool_pre_ping=True,            # Detect stale connections
    pool_size=10,
    max_overflow=20,
)

# Session factory — use via get_db() dependency
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Base class for all ORM models."""


async def get_db() -> AsyncIterator[AsyncSession]:
    """FastAPI dependency — yields a session and closes it on exit.

    Usage::

        @router.get("/items")
        async def list_items(db: AsyncSession = Depends(get_db)) -> list[Item]:
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
