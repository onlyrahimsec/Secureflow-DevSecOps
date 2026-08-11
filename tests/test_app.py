import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "app")
    )
)

from app import app


def test_homepage():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"SecureFlow" in response.data


def test_register_page():
    client = app.test_client()

    response = client.get("/register")

    assert response.status_code == 200
    assert b"Create SecureFlow Account" in response.data


def test_login_page():
    client = app.test_client()

    response = client.get("/login")

    assert response.status_code == 200
    assert b"SecureFlow Login" in response.data


def test_dashboard_requires_authentication():
    client = app.test_client()

    response = client.get("/dashboard")

    assert response.status_code == 302
    assert "/login" in response.location


def test_admin_requires_authentication():
    client = app.test_client()

    response = client.get("/admin")

    assert response.status_code == 302
    assert "/login" in response.location


def test_profile_api_requires_authentication():
    client = app.test_client()

    response = client.get("/api/profile/1")

    assert response.status_code == 401


def test_profile_api_nonexistent_user():
    client = app.test_client()

    with client.session_transaction() as session:
        session["user_id"] = 999
        session["username"] = "testuser"
        session["role"] = "user"

    response = client.get("/api/profile/999")

    assert response.status_code == 404
