from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError

from app.main import app


def test_maje_exception_handlers_are_registered():
    http_handler = app.exception_handlers[
        HTTPException
    ]
    validation_handler = app.exception_handlers[
        RequestValidationError
    ]
    general_handler = app.exception_handlers[
        Exception
    ]

    assert (
        http_handler.__name__
        == "http_exception_handler"
    )
    assert (
        validation_handler.__name__
        == "validation_exception_handler"
    )
    assert (
        general_handler.__name__
        == "general_exception_handler"
    )


from fastapi.testclient import TestClient


client = TestClient(
    app,
    raise_server_exceptions=False,
)


def test_http_exception_uses_maje_response():
    response = client.get(
        "/users/999999999",
    )

    assert response.status_code in {
        401,
        403,
        404,
    }

    body = response.json()

    assert body["success"] is False
    assert body["data"] is None
    assert "message" in body


def test_validation_error_uses_maje_response():
    response = client.post(
        "/auth/login",
        json={},
    )

    assert response.status_code == 422

    body = response.json()

    assert body["success"] is False
    assert body["message"] == "Validation failed"
    assert body["data"] is None
    assert isinstance(body["errors"], list)


def test_general_exception_uses_maje_response():
    async def raise_test_exception():
        raise RuntimeError(
            "Sensitive internal test exception"
        )

    app.add_api_route(
        "/__test/internal-error",
        raise_test_exception,
        methods=["GET"],
        include_in_schema=False,
    )

    response = client.get(
        "/__test/internal-error",
    )

    assert response.status_code == 500

    body = response.json()

    assert body == {
        "success": False,
        "message": "Internal Server Error",
        "data": None,
        "errors": None,
    }

    assert (
        "Sensitive internal test exception"
        not in response.text
    )
