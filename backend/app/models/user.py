# backend/app/models/user.py

from __future__ import annotations

from typing import TYPE_CHECKING, List

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.job import Job
    from app.models.audit_log import AuditLog


class User(Base):
    """
    ARAS User Model

    Represents recruiters and system administrators.
    """

    __tablename__ = "users"

    name: Mapped[str] = mapped_column(
        sa.String(100),
        nullable=False,
    )

    # Removed unique=True from the column to prevent Alembic clash
    # The constraint is handled safely in __table_args__ below
    email: Mapped[str] = mapped_column(
        sa.String(255),
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        sa.Text,
        nullable=False,
    )

    # Changed from Enum to String(30) to match the database exactly
    role: Mapped[str] = mapped_column(
        sa.String(30),
        nullable=False,
        default="RECRUITER",
        server_default="RECRUITER",
    )

    is_active: Mapped[bool] = mapped_column(
        sa.Boolean,
        nullable=False,
        default=True,
        server_default=sa.true(),
    )

    # ── Relationships ──────────────────────────────────────────────────────────

    jobs: Mapped[List["Job"]] = relationship(
        "Job",
        back_populates="recruiter",
        lazy="raise",
    )

    audit_logs: Mapped[List["AuditLog"]] = relationship(
        "AuditLog",
        back_populates="user",
        lazy="raise",
    )

    # ── Indexes ────────────────────────────────────────────────────────────────
    __table_args__ = (
        sa.Index("idx_users_email", "email", unique=True),
        sa.Index("idx_users_role", "role"),
        sa.Index("idx_users_is_active", "is_active"),
        {
            "comment": "Recruiters and administrators using ARAS"
        },
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, role={self.role!r})>"