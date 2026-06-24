from __future__ import annotations

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.skill import Skill
from app.repositories.exceptions import NotFoundError
from app.repositories.skill_repository import SkillRepository


@pytest.mark.asyncio
async def test_skill_repository_get_or_create(async_session: AsyncSession) -> None:
    repo = SkillRepository()

    skill = await repo.get_or_create(async_session, "Python", category="Programming")

    assert isinstance(skill, Skill)
    assert skill.skill_name == "Python"
    assert skill.category == "Programming"
    assert skill.id is not None

    same = await repo.get_or_create(async_session, "Python")
    assert same.id == skill.id
    assert same.skill_name == "Python"
    assert same.category == "Programming"

    count = await repo.count(async_session, {"skill_name": "Python"})
    assert count == 1

    fetched = await repo.get_by_name(async_session, "Python")
    assert fetched is not None
    assert fetched.id == skill.id


@pytest.mark.asyncio
async def test_skill_repository_get_by_name_or_raise(async_session: AsyncSession) -> None:
    repo = SkillRepository()

    skill = await repo.create(async_session, {"skill_name": "Docker", "category": "DevOps"})
    assert skill.skill_name == "Docker"

    fetched = await repo.get_by_name_or_raise(async_session, "Docker")
    assert fetched.id == skill.id

    with pytest.raises(NotFoundError):
        await repo.get_by_name_or_raise(async_session, "Nonexistent")
