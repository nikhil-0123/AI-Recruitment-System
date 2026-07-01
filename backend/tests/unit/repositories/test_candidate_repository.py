from __future__ import annotations

import uuid
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.candidate_repository import CandidateRepository
from app.repositories.exceptions import NotFoundError


@pytest.mark.asyncio
async def test_candidate_repository_get_by_id_or_raise(async_session: AsyncSession) -> None:
    repo = CandidateRepository()

    candidate = await repo.create(async_session, {
        "full_name": "Alice Smith",
        "email": "alice@example.com",
        "phone": "555-0100",
    })

    fetched = await repo.get_by_id_or_raise(async_session, candidate.id)
    assert fetched.id == candidate.id
    assert fetched.full_name == "Alice Smith"

    with pytest.raises(NotFoundError):
        await repo.get_by_id_or_raise(async_session, uuid.uuid4())


@pytest.mark.asyncio
async def test_candidate_repository_list_by_emails_and_get_by_email(async_session: AsyncSession) -> None:
    repo = CandidateRepository()

    await repo.create(async_session, {
        "full_name": "Bob Jones",
        "email": "bob@example.com",
    })
    await repo.create(async_session, {
        "full_name": "Carol Lee",
        "email": "carol@example.com",
    })

    candidates = await repo.list_by_emails(async_session, ["bob@example.com", "carol@example.com"])
    assert len(candidates) == 2

    candidate = await repo.get_by_email(async_session, "bob@example.com")
    assert candidate is not None
    assert candidate.full_name == "Bob Jones"
