from __future__ import annotations

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.candidate import Candidate
from app.repositories.resume_repository import ResumeRepository
from app.services.resume_service import ResumeService


@pytest.mark.asyncio
async def test_create_and_list_resumes(async_session: AsyncSession) -> None:
    service = ResumeService(repository=ResumeRepository())

    candidate = Candidate(full_name="Alice Smith", email="alice@example.com")
    async_session.add(candidate)
    await async_session.flush()

    resume = await service.create_resume(async_session, {
        "candidate_id": candidate.id,
        "file_name": "resume.pdf",
        "file_type": "application/pdf",
    })

    assert resume.id is not None
    assert resume.candidate_id == candidate.id

    items, total = await service.list_resumes(async_session, candidate_id=candidate.id)
    assert total == 1
    assert items[0].id == resume.id
