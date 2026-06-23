from __future__ import annotations

import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.job import Job
    from app.models.skill import Skill


class JobSkill(Base):
    """
    Links jobs to normalized skills and stores
    importance weights used for matching and ranking.
    """

    __tablename__ = "job_skills"

    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        sa.ForeignKey(
            "jobs.id",
            name="fk_job_skills_job_id_jobs",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    skill_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        sa.ForeignKey(
            "skills.id",
            name="fk_job_skills_skill_id_skills",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    importance_weight: Mapped[Decimal | None] = mapped_column(
        sa.Numeric(5, 2),
        nullable=True,
    )

    # Relationships

    job: Mapped["Job"] = relationship(
        "Job",
        back_populates="job_skills",
        lazy="raise",
    )

    skill: Mapped["Skill"] = relationship(
        "Skill",
        back_populates="job_skills",
        lazy="raise",
    )

    __table_args__ = (
        sa.UniqueConstraint(
            "job_id",
            "skill_id",
            name="uq_job_skills_job_skill",
        ),

        sa.CheckConstraint(
            "importance_weight >= 0",
            name="ck_job_skill_weight_min",
        ),

        sa.CheckConstraint(
            "importance_weight <= 100",
            name="ck_job_skill_weight_max",
        ),

        sa.Index(
            "idx_job_skills_job_id",
            "job_id",
        ),

        sa.Index(
            "idx_job_skills_skill_id",
            "skill_id",
        ),

        {
            "comment": (
                "Links jobs to normalized skills and stores "
                "importance weights used for matching, ranking, "
                "and explainable AI."
            )
        },
    )

    def __repr__(self) -> str:
        return f"JobSkill(id={self.id})"