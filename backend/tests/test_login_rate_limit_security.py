from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app


client = TestClient(app)


def test_login_rate_limit_rejects_excess_requests():
    assert settings.LOGIN_RATE_LIMIT == "5/minute"

    email = (
        "rate-limit-test-"
        f"{uuid4().hex}@example.com"
    )

    payload = {
        "email": email,
        "password": "Invalid-Password-2026!",
    }

    # ==============================================
    # FIRST FIVE REQUESTS ARE ALLOWED THROUGH
    # ==============================================

    for _ in range(5):
        response = client.post(
            "/auth/login",
            json=payload,
        )

        # Unknown user reaches normal authentication
        # handling, proving the request was not yet
        # blocked by the rate limiter.
        assert response.status_code == 401
        assert (
            response.json()["message"]
            == "Invalid email or password"
        )

    # ==============================================
    # SIXTH REQUEST MUST BE RATE LIMITED
    # ==============================================

    response = client.post(
        "/auth/login",
        json=payload,
    )

    assert response.status_code == 429

    body = response.json()

    assert "error" in body
    assert "Rate limit exceeded" in body["error"]
