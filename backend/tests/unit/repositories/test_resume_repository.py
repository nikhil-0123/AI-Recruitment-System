from __future__ import annotations

import uuid
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.candidate import Candidate
from app.repositories.resume_repository import ResumeRepository
from app.repositories.exceptions import NotFoundError


@pytest.mark.asyncio
async def test_resume_repository_get_by_id_or_raise(async_session: AsyncSession) -> None:
    repo = ResumeRepository()

    candidate = Candidate(
        full_name="Eve Adams",
        email="eve@example.com",
    )
    async_session.add(candidate)
    await async_session.flush()

    resume = await repo.create(async_session, {
        "candidate_id": candidate.id,
        "file_name": "resume.pdf",
        "file_type": "application/pdf",
        "file_size": 123456,
    })

    fetched = await repo.get_by_id_or_raise(async_session, resume.id)
    assert fetched.id == resume.id
    assert fetched.file_name == "resume.pdf"

    with pytest.raises(NotFoundError):
        await repo.get_by_id_or_raise(async_session, uuid.uuid4())


@pytest.mark.asyncio
async def test_resume_repository_list_by_candidate_and_get_by_ids(async_session: AsyncSession) -> None:
    repo = ResumeRepository()

    candidate = Candidate(
        full_name="Frank Miller",
        email="frank@example.com",
    )
    async_session.add(candidate)
    await async_session.flush()

    resume1 = await repo.create(async_session, {
        "candidate_id": candidate.id,
        "file_name": "resume1.pdf",
    })
    resume2 = await repo.create(async_session, {
        "candidate_id": candidate.id,
        "file_name": "resume2.pdf",
    })

    resumes = await repo.list_by_candidate(async_session, candidate.id)
    assert len(resumes) == 2

    found = await repo.get_by_ids(async_session, [resume1.id, resume2.id])
    assert {resume.id for resume in found} == {resume1.id, resume2.id}
