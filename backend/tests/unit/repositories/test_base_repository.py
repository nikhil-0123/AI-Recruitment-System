from __future__ import annotations

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base import BaseRepository
from app.repositories.filters import FilterParams
from app.repositories.pagination import PageParams
from app.repositories.sort import SortOrder, SortParams


@pytest.mark.asyncio
async def test_base_repository_crud(async_session: AsyncSession) -> None:
    repo = BaseRepository(User)

    user = await repo.create(async_session, {"name": "Alice", "email": "alice@example.com", "password_hash": "hash"})
    assert user.id is not None
    assert user.name == "Alice"

    fetched = await repo.get_by_id(async_session, user.id)
    assert fetched is not None
    assert fetched.email == "alice@example.com"

    updated = await repo.update(async_session, fetched, {"name": "Alice Smith"})
    assert updated.name == "Alice Smith"

    exists = await repo.exists(async_session, FilterParams({"email": "alice@example.com"}))
    assert exists is True

    count = await repo.count(async_session, FilterParams({"name": "Alice Smith"}))
    assert count == 1

    page = await repo.list(
        async_session,
        filters=FilterParams({"name": "Alice Smith"}),
        sort_params=SortParams(sort_by="created_at", sort_order=SortOrder.ASC),
        page_params=PageParams(page=1, page_size=10),
    )
    assert page.total == 1
    assert page.page == 1
    assert page.page_size == 10
    assert page.pages == 1
    assert page.items[0].email == "alice@example.com"

    deleted = await repo.delete(async_session, fetched)
    assert deleted.id == user.id

    missing = await repo.get_by_id(async_session, user.id)
    assert missing is None
