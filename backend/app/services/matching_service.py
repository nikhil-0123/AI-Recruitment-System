from __future__ import annotations

import uuid
from decimal import Decimal
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.candidate import Candidate
from app.models.candidate_skill import CandidateSkill
from app.models.job import Job
from app.models.job_skill import JobSkill
from app.repositories.exceptions import NotFoundError


class MatchingService:
    """Compute component scores used by the ranking engine."""

    def __init__(self) -> None:
        self.semantic_weight = 0.35
        self.skill_weight = 0.25
        self.experience_weight = 0.20
        self.education_weight = 0.10
        self.ai_weight = 0.10

    async def compute_semantic_score(
        self,
        candidate_embedding: Any,
        job_embedding: Any,
    ) -> float:
        try:
            if len(candidate_embedding) == 0 or len(job_embedding) == 0:
                return 0.0
        except (TypeError, AttributeError):
            return 0.0
        similarity = self._cosine_similarity(candidate_embedding, job_embedding)
        return max(0.0, min(100.0, similarity * 100.0))

    async def compute_skill_score(self, db: AsyncSession, candidate_id: uuid.UUID, job_id: uuid.UUID) -> float:
        candidate_skills = await self._list_candidate_skills(db, candidate_id)
        job_skills = await self._list_job_skills(db, job_id)
        if not job_skills:
            return 0.0
        candidate_skill_ids = {candidate_skill.skill_id for candidate_skill in candidate_skills}
        matches = sum(1 for job_skill in job_skills if job_skill.skill_id in candidate_skill_ids)
        return round((matches / len(job_skills)) * 100.0, 2)

    async def compute_experience_score(self, db: AsyncSession, candidate_id: uuid.UUID, job_id: uuid.UUID) -> float:
        candidate = await db.get(Candidate, candidate_id)
        job = await db.get(Job, job_id)
        if candidate is None or job is None:
            raise NotFoundError("Candidate or job", f"{candidate_id}/{job_id}")
        if job.experience_required is None or candidate.experience_years is None:
            return 0.0
        ratio = min(candidate.experience_years / Decimal(job.experience_required), Decimal("1"))
        return round(float(ratio * Decimal("100.0")), 2)

    async def compute_education_score(self, db: AsyncSession, candidate_id: uuid.UUID, job_id: uuid.UUID) -> float:
        candidate = await db.get(Candidate, candidate_id)
        job = await db.get(Job, job_id)
        if candidate is None or job is None:
            raise NotFoundError("Candidate or job", f"{candidate_id}/{job_id}")
        if not candidate.education or not job.education_required:
            return 0.0
        if candidate.education.lower() == job.education_required.lower():
            return 100.0
        return 0.0

    def _cosine_similarity(self, left: Any, right: Any) -> float:
        try:
            if len(left) != len(right):
                return 0.0
        except (TypeError, AttributeError):
            return 0.0
        
        try:
            dot = sum(float(a) * float(b) for a, b in zip(left, right))
            left_norm = sum(float(a) * float(a) for a in left) ** 0.5
            right_norm = sum(float(b) * float(b) for b in right) ** 0.5
        except (TypeError, ValueError):
            return 0.0
        
        if left_norm == 0 or right_norm == 0:
            return 0.0
        return dot / (left_norm * right_norm)

    async def _list_candidate_skills(self, db: AsyncSession, candidate_id: uuid.UUID) -> list[CandidateSkill]:
        query = select(CandidateSkill).where(CandidateSkill.candidate_id == candidate_id)
        result = await db.execute(query)
        return list(result.scalars().all())

    async def _list_job_skills(self, db: AsyncSession, job_id: uuid.UUID) -> list[JobSkill]:
        query = select(JobSkill).where(JobSkill.job_id == job_id)
        result = await db.execute(query)
        return list(result.scalars().all())
