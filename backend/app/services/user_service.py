from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserUpdate


class UserService:
    """Service encapsulating all user profile business logic."""
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def get_user_profile(self, db: AsyncSession, user_id: UUID | str) -> User:
        """
        Retrieves a user by ID.
        Raises NotFoundError if the user does not exist.
        """
        user = await self.user_repo.get_by_id_or_raise(db, user_id)
        return user

    async def update_user_profile(
        self, db: AsyncSession, user_id: UUID | str, update_data: UserUpdate | dict[str, Any]
    ) -> User:
        """
        Updates the profile of a user.
        Raises NotFoundError if the user does not exist.
        Raises ConflictError if the new email is already in use by another user.
        Only updates explicitly provided fields.
        Immutable fields (id, created_at, password_hash) are protected.
        """
        user = await self.user_repo.get_by_id_or_raise(db, user_id)

        if isinstance(update_data, UserUpdate):
            update_dict = update_data.model_dump(exclude_unset=True)
        else:
            update_dict = update_data

        protected_fields = {"id", "created_at", "password_hash"}
        filtered_update_dict = {
            k: v for k, v in update_dict.items() if k not in protected_fields
        }

        if "email" in filtered_update_dict:
            new_email = filtered_update_dict["email"]
            if new_email != user.email:
                existing_user = await self.user_repo.get_by_email(db, new_email)
                if existing_user:
                    raise ConflictError("Email already in use")

        if filtered_update_dict:
            user = await self.user_repo.update(db, user, filtered_update_dict)

        return user
