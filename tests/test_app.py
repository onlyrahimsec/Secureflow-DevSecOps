import sys
import os


sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "app"
        )
    )
)


from app import app


# ============================================================
# Homepage
# ============================================================

def test_homepage():

    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"SecureFlow" in response.data


# ============================================================
# Registration Page
# ============================================================

def test_register_page():

    client = app.test_client()

    response = client.get("/register")

    assert response.status_code == 200
    assert b"Create SecureFlow Account" in response.data


# ============================================================
# Login Page
# ============================================================

def test_login_page():

    client = app.test_client()

    response = client.get("/login")

    assert response.status_code == 200
    assert b"SecureFlow Login" in response.data


# ============================================================
# Dashboard Authentication
# ============================================================

def test_dashboard_requires_authentication():

    client = app.test_client()

    response = client.get("/dashboard")

    assert response.status_code == 302
    assert "/login" in response.location


# ============================================================
# Admin Authentication
# ============================================================

def test_admin_requires_authentication():

    client = app.test_client()

    response = client.get("/admin")

    assert response.status_code == 302
    assert "/login" in response.location


# ============================================================
# Profile API Authentication
# ============================================================

def test_profile_api_requires_authentication():

    client = app.test_client()

    response = client.get(
        "/api/profile/1"
    )

    assert response.status_code == 401


# ============================================================
# Profile API - Nonexistent User
# ============================================================

def test_profile_api_nonexistent_user():

    client = app.test_client()

    with client.session_transaction() as session:

        session["user_id"] = 999
        session["username"] = "testuser"
        session["role"] = "user"

    response = client.get(
        "/api/profile/999"
    )

    assert response.status_code == 404


# ============================================================
# Authenticated Dashboard
# ============================================================

def test_authenticated_user_can_access_dashboard():

    client = app.test_client()

    with client.session_transaction() as session:

        session["user_id"] = 1
        session["username"] = "testuser"
        session["role"] = "user"

    response = client.get(
        "/dashboard"
    )

    assert response.status_code == 200


# ============================================================
# Normal User Cannot Access Admin
# ============================================================

def test_admin_denies_normal_user():

    client = app.test_client()

    with client.session_transaction() as session:

        session["user_id"] = 1
        session["username"] = "testuser"
        session["role"] = "user"

    response = client.get(
        "/admin"
    )

    assert response.status_code == 403


# ============================================================
# Admin Can Access Admin Panel
# ============================================================

def test_admin_can_access_admin_panel():

    client = app.test_client()

    with client.session_transaction() as session:

        session["user_id"] = 1
        session["username"] = "admin"
        session["role"] = "admin"

    response = client.get(
        "/admin"
    )

    assert response.status_code == 200


# ============================================================
# Logout
# ============================================================

def test_logout_redirects_to_login():

    client = app.test_client()

    with client.session_transaction() as session:

        session["user_id"] = 1
        session["username"] = "testuser"
        session["role"] = "user"

    response = client.get(
        "/logout"
    )

    assert response.status_code == 302
    assert "/login" in response.location


# ============================================================
# Security Headers
# ============================================================

def test_security_headers():

    client = app.test_client()

    response = client.get("/")

    # MIME sniffing protection
    assert (
        response.headers.get(
            "X-Content-Type-Options"
        )
        == "nosniff"
    )

    # Clickjacking protection
    assert (
        response.headers.get(
            "X-Frame-Options"
        )
        == "DENY"
    )

    # Content Security Policy
    assert (
        response.headers.get(
            "Content-Security-Policy"
        )
        is not None
    )

    # Referrer Policy
    assert (
        response.headers.get(
            "Referrer-Policy"
        )
        == "strict-origin-when-cross-origin"
    )

    # Permissions Policy
    assert (
        response.headers.get(
            "Permissions-Policy"
        )
        is not None
    )

    # Cross-Origin Embedder Policy
    assert (
        response.headers.get(
            "Cross-Origin-Embedder-Policy"
        )
        == "require-corp"
    )

    # Cross-Origin Opener Policy
    assert (
        response.headers.get(
            "Cross-Origin-Opener-Policy"
        )
        == "same-origin"
    )

    # Cross-Origin Resource Policy
    assert (
        response.headers.get(
            "Cross-Origin-Resource-Policy"
        )
        == "same-origin"
    )

    # Cache protection
    assert (
        response.headers.get(
            "Cache-Control"
        )
        == "no-store"
    )
