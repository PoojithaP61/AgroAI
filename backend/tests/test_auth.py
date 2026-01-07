import pytest

def test_register_user(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "password123",
            "full_name": "Test User"
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["is_verified"] is False

def test_login_unverified_user(client):
    # Register first
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "password123"
        },
    )
    
    # Try login
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "testuser",
            "password": "password123",
        },
    )
    # Should fail because not verified
    assert response.status_code == 400
    assert "not verified" in response.json()["detail"]
