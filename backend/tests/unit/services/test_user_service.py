import pytest
from unittest.mock import AsyncMock
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.repositories.exceptions import NotFoundError
from app.core.exceptions import ConflictError
from app.schemas.user import UserUpdate
from app.services.user_service import UserService


@pytest.fixture
def mock_user_repo():
    return AsyncMock(spec=UserRepository)


@pytest.fixture
def mock_db_session():
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def user_service(mock_user_repo):
    return UserService(user_repo=mock_user_repo)


@pytest.fixture
def valid_user():
    return User(
        id=uuid4(),
        name="John Doe",
        email="john@example.com",
        password_hash="hashed123",
        is_active=True
    )


@pytest.mark.asyncio
async def test_get_user_profile_success(user_service, mock_db_session, mock_user_repo, valid_user):
    mock_user_repo.get_by_id_or_raise.return_value = valid_user
    
    result = await user_service.get_user_profile(mock_db_session, valid_user.id)
    
    assert result == valid_user
    mock_user_repo.get_by_id_or_raise.assert_called_once_with(mock_db_session, valid_user.id)


@pytest.mark.asyncio
async def test_get_user_profile_not_found(user_service, mock_db_session, mock_user_repo):
    user_id = uuid4()
    mock_user_repo.get_by_id_or_raise.side_effect = NotFoundError("User", user_id)
    
    with pytest.raises(NotFoundError):
        await user_service.get_user_profile(mock_db_session, user_id)


@pytest.mark.asyncio
async def test_update_user_profile_success(user_service, mock_db_session, mock_user_repo, valid_user):
    mock_user_repo.get_by_id_or_raise.return_value = valid_user
    mock_user_repo.get_by_email.return_value = None
    
    updated_user = User(
        id=valid_user.id,
        name="John Updated",
        email="john_new@example.com",
        password_hash=valid_user.password_hash,
        is_active=True
    )
    mock_user_repo.update.return_value = updated_user
    
    update_data = UserUpdate(name="John Updated", email="john_new@example.com")
    
    result = await user_service.update_user_profile(mock_db_session, valid_user.id, update_data)
    
    assert result == updated_user
    mock_user_repo.get_by_id_or_raise.assert_called_once_with(mock_db_session, valid_user.id)
    mock_user_repo.get_by_email.assert_called_once_with(mock_db_session, "john_new@example.com")
    mock_user_repo.update.assert_called_once_with(
        mock_db_session, valid_user, {"name": "John Updated", "email": "john_new@example.com"}
    )


@pytest.mark.asyncio
async def test_update_user_profile_unchanged_email(user_service, mock_db_session, mock_user_repo, valid_user):
    mock_user_repo.get_by_id_or_raise.return_value = valid_user
    
    updated_user = User(
        id=valid_user.id,
        name="John Updated",
        email="john@example.com",
        password_hash=valid_user.password_hash,
        is_active=True
    )
    mock_user_repo.update.return_value = updated_user
    
    update_data = UserUpdate(name="John Updated", email="john@example.com")
    
    result = await user_service.update_user_profile(mock_db_session, valid_user.id, update_data)
    
    assert result == updated_user
    # Ensure get_by_email is NOT called because the email didn't change
    mock_user_repo.get_by_email.assert_not_called()
    mock_user_repo.update.assert_called_once_with(
        mock_db_session, valid_user, {"name": "John Updated", "email": "john@example.com"}
    )


@pytest.mark.asyncio
async def test_update_user_profile_duplicate_email(user_service, mock_db_session, mock_user_repo, valid_user):
    mock_user_repo.get_by_id_or_raise.return_value = valid_user
    
    # Simulate that another user already has the new email
    other_user = User(id=uuid4(), email="taken@example.com")
    mock_user_repo.get_by_email.return_value = other_user
    
    update_data = UserUpdate(email="taken@example.com")
    
    with pytest.raises(ConflictError, match="Email already in use"):
        await user_service.update_user_profile(mock_db_session, valid_user.id, update_data)
        
    mock_user_repo.get_by_email.assert_called_once_with(mock_db_session, "taken@example.com")
    mock_user_repo.update.assert_not_called()


@pytest.mark.asyncio
async def test_update_user_profile_not_found(user_service, mock_db_session, mock_user_repo):
    user_id = uuid4()
    mock_user_repo.get_by_id_or_raise.side_effect = NotFoundError("User", user_id)
    update_data = UserUpdate(name="John")
    
    with pytest.raises(NotFoundError):
        await user_service.update_user_profile(mock_db_session, user_id, update_data)
