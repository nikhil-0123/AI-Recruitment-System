from __future__ import annotations

import uuid
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.job_repository import JobRepository
from app.services.job_service import JobService


@pytest.mark.asyncio
async def test_create_and_get_job(async_session: AsyncSession) -> None:
    service = JobService(repository=JobRepository())

    user = User(name="Recruiter", email="recruiter@example.com", password_hash="hash")
    async_session.add(user)
    await async_session.flush()

    job = await service.create_job(async_session, {
        "recruiter_id": user.id,
        "title": "Backend Engineer",
        "description": "Build APIs",
    })

    fetched = await service.get_job(async_session, job.id)
    assert fetched.id == job.id
    assert fetched.title == "Backend Engineer"

    with pytest.raises(Exception):
        await service.get_job(async_session, uuid.uuid4())
