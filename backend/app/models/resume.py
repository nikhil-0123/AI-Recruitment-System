from __future__ import annotations

import enum
import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.candidate import Candidate


class ParsingStatus(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Resume(Base):
    """
    Resume uploaded by or for a candidate.

    Supports:
    - Resume Upload
    - Resume Parsing
    - Skill Extraction
    - Embedding Generation
    """

    __tablename__ = "resumes"

    candidate_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        sa.ForeignKey(
            "candidates.id",
            name="fk_resumes_candidate_id_candidates",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    file_name: Mapped[str] = mapped_column(
        sa.Text,
        nullable=False,
    )

    file_url: Mapped[str | None] = mapped_column(
        sa.Text,
        nullable=True,
    )

    file_type: Mapped[str | None] = mapped_column(
        sa.String(20),
        nullable=True,
    )

    file_size: Mapped[int | None] = mapped_column(
        sa.BigInteger,
        nullable=True,
    )

    parsing_status: Mapped[ParsingStatus] = mapped_column(
        sa.Enum(ParsingStatus, name="parsing_status"),
        nullable=False,
        default=ParsingStatus.PENDING,
        server_default=ParsingStatus.PENDING.value,
    )

    uploaded_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        server_default=sa.func.now(),
    )

    # Relationships

    candidate: Mapped["Candidate"] = relationship(
        "Candidate",
        back_populates="resumes",
        lazy="raise",
    )

    __table_args__ = (
        sa.Index("idx_resumes_candidate_id", "candidate_id"),
        sa.Index("idx_resumes_parsing_status", "parsing_status"),
        {
            "comment": (
                "Candidate resume files used for parsing, "
                "skill extraction, matching, and ranking."
            )
        },
    )

    def __repr__(self) -> str:
        return (
            f"Resume("
            f"id={self.id}, "
            f"status='{self.parsing_status.value}'"
            f")"
        )