import pytest
from datetime import timedelta
from jose import jwt, ExpiredSignatureError, JWTError
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_access_token,
)
from app.core.config import settings


def test_password_hashing():
    password = "supersecretpassword123!"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert len(hashed) > 20
    assert hashed.startswith("$2")  # bcrypt prefix


def test_password_verification():
    password = "supersecretpassword123!"
    hashed = get_password_hash(password)
    
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False


def test_create_access_token():
    subject = "user123"
    token = create_access_token(subject=subject)
    
    assert isinstance(token, str)
    assert len(token) > 20
    
    # decode the token to verify claims
    payload = decode_access_token(token)
    assert payload["sub"] == subject
    assert payload["type"] == "access"
    assert "exp" in payload


def test_create_refresh_token():
    subject = "user123"
    token = create_refresh_token(subject=subject)
    
    assert isinstance(token, str)
    
    # decode the token manually since decode_access_token now enforces type="access"
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert payload["sub"] == subject
    assert payload["type"] == "refresh"


def test_decode_access_token_valid():
    subject = "user123"
    token = create_access_token(subject=subject, expires_delta=timedelta(minutes=5))
    
    payload = decode_access_token(token)
    assert payload["sub"] == subject


def test_decode_access_token_expired():
    subject = "user123"
    # Create an already expired token by passing a negative timedelta
    token = create_access_token(subject=subject, expires_delta=timedelta(minutes=-5))
    
    with pytest.raises(ExpiredSignatureError):
        decode_access_token(token)


def test_decode_access_token_invalid():
    invalid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid.signature"
    with pytest.raises(JWTError):
        decode_access_token(invalid_token)


def test_decode_access_token_rejects_refresh_token():
    subject = "user123"
    # Create a refresh token
    token = create_refresh_token(subject=subject)
    
    # Attempting to decode it as an access token should fail
    with pytest.raises(JWTError, match="Invalid token type"):
        decode_access_token(token)
