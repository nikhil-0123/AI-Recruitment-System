import pytest
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.repositories.exceptions import NotFoundError
from app.services.auth_service import AuthService, AuthenticationError
from app.core import security


@pytest.fixture
def mock_user_repo():
    return AsyncMock(spec=UserRepository)


@pytest.fixture
def mock_db_session():
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def auth_service(mock_user_repo):
    return AuthService(user_repo=mock_user_repo)


@pytest.fixture
def valid_user():
    user = User(
        id=uuid4(),
        name="Test User",
        email="test@example.com",
        password_hash="hashed_password_abc123",
        is_active=True
    )
    return user


@pytest.mark.asyncio
@patch("app.services.auth_service.security.verify_password")
async def test_authenticate_user_success(mock_verify_password, auth_service, mock_db_session, mock_user_repo, valid_user):
    mock_user_repo.get_by_email.return_value = valid_user
    mock_verify_password.return_value = True

    result = await auth_service.authenticate_user(mock_db_session, "test@example.com", "correct_password")

    assert result == valid_user
    mock_user_repo.get_by_email.assert_called_once_with(mock_db_session, "test@example.com")
    mock_verify_password.assert_called_once_with("correct_password", valid_user.password_hash)


@pytest.mark.asyncio
async def test_authenticate_user_invalid_email(auth_service, mock_db_session, mock_user_repo):
    mock_user_repo.get_by_email.return_value = None

    with pytest.raises(AuthenticationError, match="Invalid email or password"):
        await auth_service.authenticate_user(mock_db_session, "wrong@example.com", "any_password")


@pytest.mark.asyncio
@patch("app.services.auth_service.security.verify_password")
async def test_authenticate_user_invalid_password(mock_verify_password, auth_service, mock_db_session, mock_user_repo, valid_user):
    mock_user_repo.get_by_email.return_value = valid_user
    mock_verify_password.return_value = False

    with pytest.raises(AuthenticationError, match="Invalid email or password"):
        await auth_service.authenticate_user(mock_db_session, "test@example.com", "wrong_password")


@pytest.mark.asyncio
@patch("app.services.auth_service.security.verify_password")
async def test_authenticate_user_inactive(mock_verify_password, auth_service, mock_db_session, mock_user_repo, valid_user):
    valid_user.is_active = False
    mock_user_repo.get_by_email.return_value = valid_user
    mock_verify_password.return_value = True

    with pytest.raises(AuthenticationError, match="User account is inactive"):
        await auth_service.authenticate_user(mock_db_session, "test@example.com", "correct_password")


@patch("app.services.auth_service.security.create_access_token")
def test_create_access_token_for_user(mock_create_access_token, auth_service, valid_user):
    mock_create_access_token.return_value = "mocked_access_token"
    
    token = auth_service.create_access_token_for_user(valid_user)
    
    assert token == "mocked_access_token"
    mock_create_access_token.assert_called_once_with(subject=str(valid_user.id))


@patch("app.services.auth_service.security.create_refresh_token")
def test_create_refresh_token_for_user(mock_create_refresh_token, auth_service, valid_user):
    mock_create_refresh_token.return_value = "mocked_refresh_token"
    
    token = auth_service.create_refresh_token_for_user(valid_user)
    
    assert token == "mocked_refresh_token"
    mock_create_refresh_token.assert_called_once_with(subject=str(valid_user.id))


@pytest.mark.asyncio
@patch("app.services.auth_service.security.decode_refresh_token")
@patch.object(AuthService, "create_access_token_for_user")
async def test_refresh_access_token_success(mock_create_access_token, mock_decode_refresh_token, auth_service, mock_db_session, mock_user_repo, valid_user):
    mock_decode_refresh_token.return_value = {"sub": str(valid_user.id), "type": "refresh"}
    mock_user_repo.get_by_id_or_raise.return_value = valid_user
    mock_create_access_token.return_value = "new_access_token"

    result = await auth_service.refresh_access_token(mock_db_session, "valid_refresh_token")

    assert result == "new_access_token"
    mock_decode_refresh_token.assert_called_once_with("valid_refresh_token")
    mock_user_repo.get_by_id_or_raise.assert_called_once_with(mock_db_session, str(valid_user.id))
    mock_create_access_token.assert_called_once_with(valid_user)


@pytest.mark.asyncio
@patch("app.services.auth_service.security.decode_refresh_token")
async def test_refresh_access_token_invalid_type(mock_decode_refresh_token, auth_service, mock_db_session):
    mock_decode_refresh_token.side_effect = security.JWTError("Invalid token type")

    with pytest.raises(AuthenticationError, match="Invalid refresh token"):
        await auth_service.refresh_access_token(mock_db_session, "access_token")


@pytest.mark.asyncio
@patch("app.services.auth_service.security.decode_refresh_token")
async def test_refresh_access_token_expired(mock_decode_refresh_token, auth_service, mock_db_session):
    mock_decode_refresh_token.side_effect = security.ExpiredSignatureError()

    with pytest.raises(AuthenticationError, match="Refresh token has expired"):
        await auth_service.refresh_access_token(mock_db_session, "expired_token")


@pytest.mark.asyncio
@patch("app.services.auth_service.security.decode_refresh_token")
async def test_refresh_access_token_invalid(mock_decode_refresh_token, auth_service, mock_db_session):
    mock_decode_refresh_token.side_effect = security.JWTError()

    with pytest.raises(AuthenticationError, match="Invalid refresh token"):
        await auth_service.refresh_access_token(mock_db_session, "invalid_token")


@pytest.mark.asyncio
@patch("app.services.auth_service.security.decode_refresh_token")
async def test_refresh_access_token_user_not_found(mock_decode_refresh_token, auth_service, mock_db_session, mock_user_repo):
    mock_decode_refresh_token.return_value = {"sub": "non_existent_id", "type": "refresh"}
    mock_user_repo.get_by_id_or_raise.side_effect = NotFoundError("User", "non_existent_id")

    with pytest.raises(AuthenticationError, match="User not found"):
        await auth_service.refresh_access_token(mock_db_session, "valid_token_deleted_user")


@pytest.mark.asyncio
@patch("app.services.auth_service.security.decode_refresh_token")
async def test_refresh_access_token_user_inactive(mock_decode_refresh_token, auth_service, mock_db_session, mock_user_repo, valid_user):
    valid_user.is_active = False
    mock_decode_refresh_token.return_value = {"sub": str(valid_user.id), "type": "refresh"}
    mock_user_repo.get_by_id_or_raise.return_value = valid_user

    with pytest.raises(AuthenticationError, match="User account is inactive"):
        await auth_service.refresh_access_token(mock_db_session, "valid_token_inactive_user")


@pytest.mark.asyncio
@patch("app.services.auth_service.security.get_password_hash")
async def test_register_success(mock_get_password_hash, auth_service, mock_db_session, mock_user_repo, valid_user):
    from app.schemas.auth import UserCreate
    
    request = UserCreate(
        name="New User",
        email="new@example.com",
        password="password123"
    )
    
    mock_user_repo.get_by_email.return_value = None
    mock_get_password_hash.return_value = "hashed_pass"
    mock_user_repo.create.return_value = valid_user
    
    result = await auth_service.register(mock_db_session, request)
    
    assert result == valid_user
    mock_user_repo.get_by_email.assert_called_once_with(mock_db_session, "new@example.com")
    mock_get_password_hash.assert_called_once_with("password123")
    mock_user_repo.create.assert_called_once_with(
        mock_db_session,
        {
            "email": "new@example.com",
            "name": "New User",
            "password_hash": "hashed_pass",
        }
    )


@pytest.mark.asyncio
async def test_register_conflict(auth_service, mock_db_session, mock_user_repo, valid_user):
    from app.schemas.auth import UserCreate
    from app.core.exceptions import ConflictError
    
    request = UserCreate(
        name="Existing User",
        email="test@example.com",
        password="password123"
    )
    
    mock_user_repo.get_by_email.return_value = valid_user
    
    with pytest.raises(ConflictError, match="Email already registered"):
        await auth_service.register(mock_db_session, request)
