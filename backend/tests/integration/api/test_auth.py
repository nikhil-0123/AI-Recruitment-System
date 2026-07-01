import pytest
from httpx import AsyncClient

from app.models.user import User


@pytest.mark.asyncio
async def test_register_success(client: AsyncClient):
    payload = {
        "name": "New Integration User",
        "email": "new_integration@example.com",
        "password": "strongpassword123"
    }
    
    response = await client.post("/api/v1/auth/register", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "New Integration User"
    assert data["email"] == "new_integration@example.com"
    assert "id" in data
    assert "role" in data
    assert data["is_active"] is True


@pytest.mark.asyncio
async def test_register_duplicate(client: AsyncClient, authenticated_test_user: User):
    payload = {
        "name": "Another User",
        "email": authenticated_test_user.email,  # Using the email of the existing test user
        "password": "strongpassword123"
    }
    
    response = await client.post("/api/v1/auth/register", json=payload)
    
    assert response.status_code == 409
    body = response.json()

    assert body["success"] is False
    assert body["message"] == "Email already registered"
    assert body["errors"] == []


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, authenticated_test_user: User):
    # The authenticated_test_user fixture is created with password "password123"
    payload = {
        "email": authenticated_test_user.email,
        "password": "password123"
    }
    
    response = await client.post("/api/v1/auth/login", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient, authenticated_test_user: User):
    payload = {
        "email": authenticated_test_user.email,
        "password": "wrongpassword"
    }
    
    response = await client.post("/api/v1/auth/login", json=payload)
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_refresh_success(client: AsyncClient, authenticated_test_user: User):
    # First login to get a valid refresh token
    login_payload = {
        "email": authenticated_test_user.email,
        "password": "password123"
    }
    login_response = await client.post("/api/v1/auth/login", json=login_payload)
    assert login_response.status_code == 200
    refresh_token = login_response.json()["refresh_token"]
    
    # Now use the refresh token
    refresh_payload = {
        "refresh_token": refresh_token
    }
    response = await client.post("/api/v1/auth/refresh", json=refresh_payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.asyncio
async def test_refresh_unauthorized(client: AsyncClient):
    refresh_payload = {
        "refresh_token": "invalid_refresh_token_string"
    }
    response = await client.post("/api/v1/auth/refresh", json=refresh_payload)
    
    assert response.status_code == 401
