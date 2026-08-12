import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "app")
    )
)

from app import app


# ============================================================
# Basic Application Tests
# ============================================================

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


# ============================================================
# Authentication & Access Control Tests
# ============================================================

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

    data = response.get_json()

    assert data["error"] == "Authentication required"


# ============================================================
# API Access Control Tests
# ============================================================

def test_profile_api_nonexistent_user():
    client = app.test_client()

    with client.session_transaction() as session:
        session["user_id"] = 999
        session["username"] = "testuser"
        session["role"] = "user"

    response = client.get("/api/profile/999")

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "User not found"


def test_profile_api_prevents_user_access_to_other_user():
    client = app.test_client()

    with client.session_transaction() as session:
        session["user_id"] = 1
        session["username"] = "testuser"
        session["role"] = "user"

    response = client.get("/api/profile/999")

    assert response.status_code == 403

    data = response.get_json()

    assert data["error"] == "Access denied"


# ============================================================
# Security Header Regression Tests
# ============================================================

def test_security_headers():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200

    # Prevent MIME-type sniffing
    assert response.headers.get(
        "X-Content-Type-Options"
    ) == "nosniff"

    # Prevent clickjacking
    assert response.headers.get(
        "X-Frame-Options"
    ) == "DENY"

    # Content Security Policy
    assert response.headers.get(
        "Content-Security-Policy"
    ) is not None


# ============================================================
# Health Check
# ============================================================

def test_health_endpoint():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "ok"
    assert data["service"] == "SecureFlow"


# ============================================================
# Logout Test
# ============================================================

def test_logout_redirects_to_login():
    client = app.test_client()

    response = client.get("/logout")

    assert response.status_code == 302
    assert "/login" in response.location


# ============================================================
# Authenticated Dashboard Test
# ============================================================

def test_authenticated_user_can_access_dashboard():
    client = app.test_client()

    with client.session_transaction() as session:
        session["user_id"] = 1
        session["username"] = "testuser"
        session["role"] = "user"

    response = client.get("/dashboard")

    assert response.status_code == 200


# ============================================================
# Admin Authorization Test
# ============================================================

def test_admin_access_requires_admin_role():
    client = app.test_client()

    with client.session_transaction() as session:
        session["user_id"] = 1
        session["username"] = "testuser"
        session["role"] = "user"

    response = client.get("/admin")

    assert response.status_code == 403


# ============================================================
# Admin Access Test
# ============================================================

def test_admin_can_access_admin_panel():
    client = app.test_client()

    with client.session_transaction() as session:
        session["user_id"] = 1
        session["username"] = "admin"
        session["role"] = "admin"

    response = client.get("/admin")

    assert response.status_code == 200
