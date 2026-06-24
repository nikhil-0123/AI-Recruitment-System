from __future__ import annotations

import uuid
from datetime import datetime, timezone

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    """
    Shared SQLAlchemy 2.0 declarative base for all ARAS ORM models.

    Provides every table with:
      - id          : UUID PK, server default uuid_generate_v4()
      - created_at  : immutable insert timestamp
      - updated_at  : auto-updated on every UPDATE

    All tables inherit this class.
    Never call Base.metadata.create_all() — always use Alembic.
    """

    type_annotation_map = {
        uuid.UUID: UUID(as_uuid=True),
    }

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.uuid_generate_v4(),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id})>"
