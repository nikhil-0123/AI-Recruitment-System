from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base import BaseRepository
from app.repositories.exceptions import NotFoundError


class UserRepository(BaseRepository[User]):
    def __init__(self) -> None:
        super().__init__(User)

    async def get_by_id_or_raise(
        self,
        db: AsyncSession,
        user_id: object,
    ) -> User:
        user = await self.get_by_id(db, user_id)
        if user is None:
            raise NotFoundError("User", user_id)
        return user

    async def get_by_email(
        self,
        db: AsyncSession,
        email: str,
    ) -> Optional[User]:
        query = select(User).where(User.email == email)
        result = await db.execute(query)
        return result.scalars().first()
