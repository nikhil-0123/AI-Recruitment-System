from __future__ import annotations

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.candidate import Candidate
from app.models.skill import Skill
from app.models.candidate_skill import CandidateSkill
from app.repositories.candidate_skill_repository import CandidateSkillRepository


@pytest.mark.asyncio
async def test_candidate_skill_repository_list_and_get_by_candidate(async_session: AsyncSession) -> None:
    repo = CandidateSkillRepository()

    candidate = Candidate(full_name="Test Candidate", email="test@example.com")
    async_session.add(candidate)

    skill = Skill(skill_name="SQL", category="Database")
    async_session.add(skill)

    await async_session.flush()

    candidate_skill = await repo.create(async_session, {
        "candidate_id": candidate.id,
        "skill_id": skill.id,
        "proficiency_score": 82.5,
    })

    fetched = await repo.get_by_candidate_and_skill(async_session, candidate.id, skill.id)
    assert fetched is not None
    assert fetched.id == candidate_skill.id

    candidate_skills = await repo.list_by_candidate(async_session, candidate.id)
    assert len(candidate_skills) == 1
    assert candidate_skills[0].candidate_id == candidate.id

    skill_list = await repo.list_by_skill(async_session, skill.id)
    assert len(skill_list) == 1
    assert skill_list[0].skill_id == skill.id
