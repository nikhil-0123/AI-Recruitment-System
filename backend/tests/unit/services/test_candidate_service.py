from __future__ import annotations

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.candidate_repository import CandidateRepository
from app.services.candidate_service import CandidateService


@pytest.mark.asyncio
async def test_create_and_list_candidates(async_session: AsyncSession) -> None:
    service = CandidateService(repository=CandidateRepository())

    candidate = await service.create_candidate(async_session, {
        "full_name": "Alice Smith",
        "email": "alice@example.com",
    })

    assert candidate.id is not None
    assert candidate.full_name == "Alice Smith"

    items, total = await service.list_candidates(async_session)
    assert total >= 1
    assert any(item.id == candidate.id for item in items)
