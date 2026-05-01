def test_login_invalid_credentials(client):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "wronguser", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

def test_login_missing_fields(client):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "someuser"}
    )
    assert response.status_code == 422 # FastAPI validation error for missing field

from backend.models import User

def test_register_duplicate_user(client, db_session):
    # 1. First we manually insert a verified user into the test database
    test_user = User(
        email="test_duplicate@example.com",
        username="test_duplicate",
        hashed_password="hashed_password",
        is_active=True,
        is_verified=True
    )
    db_session.add(test_user)
    db_session.commit()

    # 2. Try to register with the exact same email
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test_duplicate@example.com",
            "username": "new_username",
            "password": "Password123!"
        }
    )
    
    # This should fail since the email is in the DB
    assert response.status_code == 400
    assert "already" in response.json()["detail"].lower()
    
    # Clean up
    db_session.delete(test_user)
    db_session.commit()

def test_health_check(client):
    response = client.get("/api/v1/health")
    if response.status_code == 200:
        assert response.json() == {"status": "ok"}
