from pydantic import BaseModel, ConfigDict, EmailStr, Field


class LoginRequest(BaseModel):
    """Schema for user login requests."""
    email: EmailStr = Field(..., description="The user's registered email address")
    password: str = Field(..., description="The user's raw password")
    
    model_config = ConfigDict(extra="forbid")


class TokenResponse(BaseModel):
    """Schema for returning JWT tokens."""
    access_token: str = Field(..., description="The JWT access token")
    refresh_token: str = Field(..., description="The JWT refresh token")
    token_type: str = Field(default="bearer", description="The token type (usually Bearer)")


class RefreshTokenRequest(BaseModel):
    """Schema for requesting a new access token via refresh token."""
    refresh_token: str = Field(..., description="The previously issued refresh token")
    
    model_config = ConfigDict(extra="forbid")


class UserCreate(BaseModel):
    """Schema for registering a new user."""
    name: str = Field(..., min_length=2, description="The user's full name")
    email: EmailStr = Field(..., description="The user's email address")
    password: str = Field(..., min_length=8, description="The user's raw password (min 8 characters)")
    
    model_config = ConfigDict(extra="forbid")
