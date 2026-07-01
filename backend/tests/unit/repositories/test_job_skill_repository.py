from __future__ import annotations

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job import Job
from app.models.skill import Skill
from app.models.user import User
from app.repositories.job_skill_repository import JobSkillRepository


@pytest.mark.asyncio
async def test_job_skill_repository_list_and_get_by_job(async_session: AsyncSession) -> None:
    repo = JobSkillRepository()

    user = User(name="Recruiter", email="recruiter@example.com", password_hash="hash")
    async_session.add(user)

    await async_session.flush()

    job = Job(
        recruiter_id=user.id,
        title="Test Job",
        description="Description",
    )
    async_session.add(job)

    skill = Skill(skill_name="Python", category="Programming")
    async_session.add(skill)

    await async_session.flush()

    job_skill = await repo.create(async_session, {
        "job_id": job.id,
        "skill_id": skill.id,
        "importance_weight": 75.0,
    })

    fetched = await repo.get_by_job_and_skill(async_session, job.id, skill.id)
    assert fetched is not None
    assert fetched.id == job_skill.id

    job_skills = await repo.list_by_job(async_session, job.id)
    assert len(job_skills) == 1

    skill_list = await repo.list_by_skill(async_session, skill.id)
    assert len(skill_list) == 1
    assert skill_list[0].skill_id == skill.id
