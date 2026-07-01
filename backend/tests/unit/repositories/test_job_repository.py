from __future__ import annotations

import uuid
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.exceptions import NotFoundError
from app.repositories.job_repository import JobRepository


@pytest.mark.asyncio
async def test_job_repository_get_by_id_or_raise(async_session: AsyncSession) -> None:
    repo = JobRepository()

    user = User(name="Recruiter", email="recruiter@example.com", password_hash="hash")
    async_session.add(user)
    await async_session.flush()

    job = await repo.create(async_session, {
        "recruiter_id": user.id,
        "title": "Backend Engineer",
        "description": "Build APIs",
    })

    fetched = await repo.get_by_id_or_raise(async_session, job.id)
    assert fetched.id == job.id
    assert fetched.title == "Backend Engineer"

    with pytest.raises(NotFoundError):
        await repo.get_by_id_or_raise(async_session, uuid.uuid4())


@pytest.mark.asyncio
async def test_job_repository_list_by_recruiter(async_session: AsyncSession) -> None:
    repo = JobRepository()

    user = User(name="Recruiter2", email="recruiter2@example.com", password_hash="hash")
    async_session.add(user)
    await async_session.flush()

    await repo.create(async_session, {
        "recruiter_id": user.id,
        "title": "Job A",
        "description": "Desc A",
        "status": "published",
    })
    await repo.create(async_session, {
        "recruiter_id": user.id,
        "title": "Job B",
        "description": "Desc B",
        "status": "draft",
    })

    published = await repo.list_by_recruiter(async_session, user.id, status="published")
    assert len(published) == 1
    assert published[0].status == "published"

    all_jobs = await repo.list_by_recruiter(async_session, user.id, sort_desc=False)
    assert len(all_jobs) == 2


@pytest.mark.asyncio
async def test_job_repository_get_by_ids(async_session: AsyncSession) -> None:
    repo = JobRepository()

    user = User(name="Recruiter3", email="recruiter3@example.com", password_hash="hash")
    async_session.add(user)
    await async_session.flush()

    job1 = await repo.create(async_session, {
        "recruiter_id": user.id,
        "title": "Job 1",
        "description": "Desc 1",
    })
    job2 = await repo.create(async_session, {
        "recruiter_id": user.id,
        "title": "Job 2",
        "description": "Desc 2",
    })

    jobs = await repo.get_by_ids(async_session, [job1.id, job2.id])
    assert {job.id for job in jobs} == {job1.id, job2.id}
