from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.core.enums import UserRole


class UserResponse(BaseModel):
    """Schema for returning user data."""
    id: UUID = Field(description="The unique identifier of the user")
    name: str = Field(description="The user's full name")
    email: EmailStr = Field(description="The user's email address")
    role: UserRole = Field(description="The user's role (e.g., admin, recruiter)")
    is_active: bool = Field(description="Whether the user account is active")
    created_at: datetime = Field(description="When the user was created")
    updated_at: datetime = Field(description="When the user was last updated")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class UserUpdate(BaseModel):
    """Schema for updating a user's basic profile."""
    name: str | None = Field(None, min_length=2, description="The user's new full name")
    email: EmailStr | None = Field(None, description="The user's new email address")
    
    model_config = ConfigDict(extra="forbid")


class ChangePasswordRequest(BaseModel):
    """Schema for changing a user's password."""
    current_password: str = Field(..., description="The user's current password")
    new_password: str = Field(..., min_length=8, description="The new password (min 8 characters)")
    
    model_config = ConfigDict(extra="forbid")
