from __future__ import annotations

import uuid
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.candidate import Candidate
    from app.models.skill import Skill


class CandidateSkill(Base):
    """
    ORM model for the `candidate_skills` table.
    Source: 08_Database_Design.md Section 10

    Column            | Type           | Constraint
    --------------------------------------------------
    id                | UUID           | PK (from Base)
    candidate_id      | UUID           | FK → candidates.id NOT NULL
    skill_id          | UUID           | FK → skills.id NOT NULL
    proficiency_score | NUMERIC(5,2)   | nullable

    NOTE: The prompt field `skill_name` is NOT used here.
          The document uses a proper FK skill_id → skills.id
          to avoid data duplication and enable skill analytics.
    NOTE: The prompt field `confidence_score` maps to
          `proficiency_score` per 08_Database_Design.md.
    """

    __tablename__ = "candidate_skills"

    candidate_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        sa.ForeignKey(
            "candidates.id",
            ondelete="CASCADE",
            name="fk_candidate_skills_candidate_id_candidates",
        ),
        nullable=False,
    )

    skill_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        sa.ForeignKey(
            "skills.id",
            ondelete="CASCADE",
            name="fk_candidate_skills_skill_id_skills",
        ),
        nullable=False,
    )

    proficiency_score: Mapped[Optional[Decimal]] = mapped_column(
        sa.Numeric(5, 2),
        nullable=True,
    )

    # ── Relationships ──────────────────────────────────────────────────────────
    candidate: Mapped["Candidate"] = relationship(
        "Candidate",
        back_populates="candidate_skills",
        lazy="raise",
    )

    skill: Mapped["Skill"] = relationship(
        "Skill",
        back_populates="candidate_skills",
        lazy="raise",
    )

    # ── Indexes & Constraints ──────────────────────────────────────────────────
    __table_args__ = (
        # Prevent duplicate skill entries per candidate
        sa.UniqueConstraint(
            "candidate_id",
            "skill_id",
            name="uq_candidate_skills_candidate_skill",
        ),

        sa.CheckConstraint(
            "proficiency_score >= 0",
            name="ck_candidate_skill_score_min",
        ),

        sa.CheckConstraint(
            "proficiency_score <= 100",
            name="ck_candidate_skill_score_max",
        ),

        sa.Index("idx_candidate_skills_candidate_id", "candidate_id"),
        sa.Index("idx_candidate_skills_skill_id", "skill_id"),
    )

    def __repr__(self) -> str:
        return (
            f"<CandidateSkill(candidate_id={self.candidate_id}, "
            f"skill_id={self.skill_id})>"
        )