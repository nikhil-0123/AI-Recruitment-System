from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.core import security
from app.core.exceptions import ARASBaseException


class AuthenticationError(ARASBaseException):
    """Domain exception raised for any authentication failure."""
    def __init__(self, message: str = "Invalid credentials"):
        # Status code 401 is hardcoded to avoid importing fastapi.status in the service layer
        super().__init__(message=message, status_code=401)


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def authenticate_user(self, db: AsyncSession, email: str, password: str) -> User:
        """
        Authenticates a user by email and password.
        Raises AuthenticationError if invalid or inactive.
        """
        user = await self.user_repo.get_by_email(db, email)
        if not user:
            raise AuthenticationError("Invalid email or password")
        
        if not security.verify_password(password, user.password_hash):
            raise AuthenticationError("Invalid email or password")
            
        if not user.is_active:
            raise AuthenticationError("User account is inactive")
            
        return user

    def create_access_token_for_user(self, user: User) -> str:
        """Creates a JWT access token for the given user."""
        return security.create_access_token(subject=str(user.id))

    def create_refresh_token_for_user(self, user: User) -> str:
        """Creates a JWT refresh token for the given user."""
        return security.create_refresh_token(subject=str(user.id))

    async def refresh_access_token(self, db: AsyncSession, refresh_token: str) -> str:
        """
        Validates a refresh token and issues a new access token.
        Raises AuthenticationError if the token is invalid or the user no longer exists/is inactive.
        """
        try:
            # JWT decoding delegated entirely to security.py
            payload = security.decode_refresh_token(refresh_token)
            
            user_id = payload.get("sub")
            if not user_id:
                raise AuthenticationError("Invalid token payload")
                
        except security.ExpiredSignatureError:
            raise AuthenticationError("Refresh token has expired")
        except security.JWTError:
            raise AuthenticationError("Invalid refresh token")
            
        # Verify the user still exists and is active
        from app.repositories.exceptions import NotFoundError
        try:
            user = await self.user_repo.get_by_id_or_raise(db, user_id)
        except NotFoundError:
            raise AuthenticationError("User not found")
            
        if not user.is_active:
            raise AuthenticationError("User account is inactive")
            
        return self.create_access_token_for_user(user)
