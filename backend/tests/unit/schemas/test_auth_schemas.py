import uuid
from datetime import datetime
import pytest
from pydantic import ValidationError

from app.schemas.auth import LoginRequest, TokenResponse, RefreshTokenRequest, UserCreate
from app.schemas.user import UserResponse, UserUpdate, ChangePasswordRequest


def test_login_request_valid():
    schema = LoginRequest(email="test@example.com", password="password123")
    assert schema.email == "test@example.com"
    assert schema.password == "password123"


def test_login_request_invalid_email():
    with pytest.raises(ValidationError) as exc_info:
        LoginRequest(email="not-an-email", password="password123")
    assert "value is not a valid email address" in str(exc_info.value).lower() or "email" in str(exc_info.value).lower()


def test_user_create_valid():
    schema = UserCreate(name="John Doe", email="john@example.com", password="securepassword123")
    assert schema.name == "John Doe"
    assert schema.email == "john@example.com"
    assert schema.password == "securepassword123"


def test_user_create_invalid_password():
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(name="John Doe", email="john@example.com", password="short")
    assert "string should have at least 8 characters" in str(exc_info.value).lower() or "min_length" in str(exc_info.value).lower()


def test_user_create_invalid_name():
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(name="J", email="john@example.com", password="securepassword123")
    assert "string should have at least 2 characters" in str(exc_info.value).lower() or "min_length" in str(exc_info.value).lower()


def test_token_response_serialization():
    schema = TokenResponse(access_token="access_abc123", refresh_token="refresh_abc123")
    assert schema.access_token == "access_abc123"
    assert schema.refresh_token == "refresh_abc123"
    assert schema.token_type == "bearer"
    
    dumped = schema.model_dump()
    assert dumped["access_token"] == "access_abc123"
    assert dumped["refresh_token"] == "refresh_abc123"
    assert dumped["token_type"] == "bearer"


def test_refresh_token_request_valid():
    schema = RefreshTokenRequest(refresh_token="my_refresh_token")
    assert schema.refresh_token == "my_refresh_token"


def test_user_response_from_attributes():
    class DummyDBUser:
        def __init__(self):
            self.id = uuid.uuid4()
            self.name = "Alice User"
            self.email = "alice@example.com"
            self.role = "recruiter"
            self.is_active = True
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            self.password_hash = "hashed_password"  # Should NOT be in the schema

    db_user = DummyDBUser()
    schema = UserResponse.model_validate(db_user)
    
    assert schema.id == db_user.id
    assert schema.name == "Alice User"
    assert schema.email == "alice@example.com"
    assert schema.role == "recruiter"
    
    # Ensure password_hash is not present in the response
    dumped = schema.model_dump()
    assert "password_hash" not in dumped
    assert "password" not in dumped


def test_user_update_valid():
    schema = UserUpdate(name="Jane Doe")
    assert schema.name == "Jane Doe"
    assert schema.email is None

    schema2 = UserUpdate(email="jane@example.com")
    assert schema2.name is None
    assert schema2.email == "jane@example.com"


def test_change_password_request_invalid():
    with pytest.raises(ValidationError):
        ChangePasswordRequest(current_password="old", new_password="short")
