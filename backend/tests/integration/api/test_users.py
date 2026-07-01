import pytest
from httpx import AsyncClient

from app.models.user import User


@pytest.mark.asyncio
async def test_get_me_success(client: AsyncClient, authenticated_test_user: User, auth_header: dict[str, str]):
    response = await client.get("/api/v1/users/me", headers=auth_header)
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(authenticated_test_user.id)
    assert data["email"] == authenticated_test_user.email
    assert data["name"] == authenticated_test_user.name


@pytest.mark.asyncio
async def test_get_me_unauthenticated(client: AsyncClient):
    response = await client.get("/api/v1/users/me")
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_update_me_success(client: AsyncClient, authenticated_test_user: User, auth_header: dict[str, str]):
    payload = {
        "name": "Updated User Name",
        "email": "updated_email@example.com"
    }
    
    response = await client.put("/api/v1/users/me", headers=auth_header, json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(authenticated_test_user.id)
    assert data["name"] == "Updated User Name"
    assert data["email"] == "updated_email@example.com"


@pytest.mark.asyncio
async def test_update_me_duplicate_email(client: AsyncClient, authenticated_test_user: User, auth_header: dict[str, str]):
    # First register another user directly via API
    other_user_payload = {
        "name": "Other User",
        "email": "other@example.com",
        "password": "password123"
    }
    await client.post("/api/v1/auth/register", json=other_user_payload)
    
    # Now try to update the authenticated user to use the other user's email
    payload = {
        "email": "other@example.com"
    }
    
    response = await client.put("/api/v1/users/me", headers=auth_header, json=payload)
    
    assert response.status_code == 409
    assert response.json()["message"] == "Email already in use"
    assert response.json()["success"] is False
    assert response.json()["errors"] == []


@pytest.mark.asyncio
async def test_update_me_validation_failure(client: AsyncClient, auth_header: dict[str, str]):
    # Provide an invalid email format
    payload = {
        "email": "not_an_email"
    }
    
    response = await client.put("/api/v1/users/me", headers=auth_header, json=payload)
    
    assert response.status_code == 422  # Unprocessable Entity (Pydantic validation error)
