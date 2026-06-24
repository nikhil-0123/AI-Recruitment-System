# backend/app/models/resume.py

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.candidate import Candidate


class Resume(Base):
    """
    ORM model for the `resumes` table.
    Source: 08_Database_Design.md Section 8

    Column         | Type          | Constraint
    -----------------------------------------------
    id             | UUID          | PK (from Base)
    candidate_id   | UUID          | FK → candidates.id NOT NULL
    file_name      | TEXT          | NOT NULL
    file_url       | TEXT          | nullable
    file_type      | VARCHAR(20)   | nullable
    file_size      | BIGINT        | nullable
    parsing_status | VARCHAR(50)   | NOT NULL DEFAULT 'pending'
    uploaded_at    | TIMESTAMPTZ   | NOT NULL DEFAULT NOW()

    NOTE: Document column is `file_url` NOT `file_path`.
    NOTE: Document column is `parsing_status` NOT `upload_status`.
    NOTE: Document timestamp is `uploaded_at` NOT `created_at`.
    """

    __tablename__ = "resumes"

    candidate_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        sa.ForeignKey(
            "candidates.id",
            ondelete="CASCADE",
            name="fk_resumes_candidate_id_candidates",
        ),
        nullable=False,
    )

    file_name: Mapped[str] = mapped_column(
        sa.Text,
        nullable=False,
    )

    file_url: Mapped[Optional[str]] = mapped_column(
        sa.Text,
        nullable=True,
    )

    file_type: Mapped[Optional[str]] = mapped_column(
        sa.String(20),
        nullable=True,
    )

    file_size: Mapped[Optional[int]] = mapped_column(
        sa.BigInteger,
        nullable=True,
    )

    parsing_status: Mapped[str] = mapped_column(
        sa.String(50),
        nullable=False,
        default="pending",
        server_default="pending",
    )

    uploaded_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        server_default=sa.func.now(),
    )

    # ── Relationships ──────────────────────────────────────────────────────────
    candidate: Mapped["Candidate"] = relationship(
        "Candidate",
        back_populates="resumes",
        lazy="raise",
    )

    # ── Indexes ────────────────────────────────────────────────────────────────
    __table_args__ = (
        sa.Index("idx_resumes_candidate_id", "candidate_id"),
        sa.Index("idx_resumes_parsing_status", "parsing_status"),
    )

    def __repr__(self) -> str:
        return (
            f"<Resume(id={self.id}, "
            f"parsing_status={self.parsing_status!r})>"
        )