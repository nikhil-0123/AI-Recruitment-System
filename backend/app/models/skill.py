from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.candidate_skill import CandidateSkill
    from app.models.job_skill import JobSkill


class Skill(Base):
    """
    Master catalog of normalized skills.

    Examples:
    - Python
    - FastAPI
    - PostgreSQL
    - Docker
    - AWS

    Used by:
    - candidate_skills
    - job_skills
    - matching engine
    - ranking engine
    - explainable AI (XAI)
    """

    __tablename__ = "skills"

    skill_name: Mapped[str] = mapped_column(
        sa.String(100),
        nullable=False,
        unique=True,
    )

    category: Mapped[str | None] = mapped_column(
        sa.String(100),
        nullable=True,
    )

    # Relationships

    candidate_skills: Mapped[list["CandidateSkill"]] = relationship(
        "CandidateSkill",
        back_populates="skill",
        lazy="raise",
    )

    job_skills: Mapped[list["JobSkill"]] = relationship(
        "JobSkill",
        back_populates="skill",
        lazy="raise",
    )

    __table_args__ = (
        sa.Index("idx_skills_category", "category"),
        {
            "comment": (
                "Master catalog of normalized skills used for "
                "candidate matching, ranking, and explainable AI."
            )
        },
    )

    def __repr__(self) -> str:
        return (
            f"Skill("
            f"id={self.id}, "
            f"skill_name='{self.skill_name}'"
            f")"
        )