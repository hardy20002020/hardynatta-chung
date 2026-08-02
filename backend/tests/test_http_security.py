from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_security_headers_are_present():
    response = client.get("/")

    assert response.status_code == 200

    assert (
        response.headers["X-Content-Type-Options"]
        == "nosniff"
    )
    assert (
        response.headers["X-Frame-Options"]
        == "DENY"
    )
    assert (
        response.headers["Referrer-Policy"]
        == "no-referrer"
    )
    assert (
        response.headers["Permissions-Policy"]
        == "camera=(), microphone=(), geolocation=()"
    )
    assert (
        response.headers["Content-Security-Policy"]
        == "default-src 'none'; frame-ancestors 'none'"
    )


def test_untrusted_host_is_rejected():
    response = client.get(
        "/",
        headers={
            "host": "evil.example.com",
        },
    )

    assert response.status_code == 400
    assert response.text == "Invalid host header"


def test_allowed_cors_origin_is_accepted():
    response = client.options(
        "/auth/login",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers":
                "Authorization,Content-Type",
        },
    )

    assert response.status_code == 200

    assert (
        response.headers["Access-Control-Allow-Origin"]
        == "http://localhost:5173"
    )

    assert (
        response.headers["Access-Control-Allow-Credentials"]
        == "true"
    )


def test_disallowed_cors_origin_is_not_accepted():
    response = client.options(
        "/auth/login",
        headers={
            "Origin": "https://evil.example.com",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert (
        response.headers.get(
            "Access-Control-Allow-Origin"
        )
        != "https://evil.example.com"
    )


def test_disallowed_cors_method_is_rejected():
    response = client.options(
        "/auth/login",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "PATCH",
        },
    )

    assert response.status_code == 400


def test_hsts_is_disabled_in_development(monkeypatch):
    monkeypatch.setattr(
        "app.core.security_headers.settings.ENVIRONMENT",
        "development",
    )

    response = client.get("/")

    assert response.status_code == 200
    assert (
        "Strict-Transport-Security"
        not in response.headers
    )


def test_hsts_is_enabled_in_production(monkeypatch):
    monkeypatch.setattr(
        "app.core.security_headers.settings.ENVIRONMENT",
        "production",
    )

    response = client.get("/")

    assert response.status_code == 200
    assert (
        response.headers["Strict-Transport-Security"]
        == (
            "max-age=31536000; "
            "includeSubDomains"
        )
    )
