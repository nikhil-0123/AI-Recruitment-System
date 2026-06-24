from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.skill import Skill
from app.repositories.base import BaseRepository
from app.repositories.exceptions import NotFoundError


class SkillRepository(BaseRepository[Skill]):
    def __init__(self) -> None:
        super().__init__(Skill)

    async def get_by_name(
        self,
        db: AsyncSession,
        skill_name: str,
    ) -> Optional[Skill]:
        query = select(Skill).where(Skill.skill_name == skill_name)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_by_name_or_raise(
        self,
        db: AsyncSession,
        skill_name: str,
    ) -> Skill:
        skill = await self.get_by_name(db, skill_name)
        if skill is None:
            raise NotFoundError("Skill", skill_name)
        return skill

    async def get_or_create(
        self,
        db: AsyncSession,
        skill_name: str,
        category: str | None = None,
    ) -> Skill:
        existing = await self.get_by_name(db, skill_name)
        if existing:
            if category is not None and existing.category != category:
                existing.category = category
                await db.flush()
            return existing

        return await self.create(db, {"skill_name": skill_name, "category": category})
