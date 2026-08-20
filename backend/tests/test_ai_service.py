from app.ai.gateway import ModelGateway
from app.ai.exceptions import (
    AIGatewayError,
    AIInvalidOutputError,
    AIServiceDisabledError,
)
from app.ai.service import AIService


class FakeModelGateway(ModelGateway):
    def generate(self, prompt: str) -> str:
        return f"fake response: {prompt}"


def test_ai_service_uses_injected_model_gateway():
    service = AIService(
        gateway=FakeModelGateway()
    )

    result = service.generate(
        "Hello MAJE"
    )

    assert result == "fake response: Hello MAJE"


def test_ai_service_rejects_prompt_above_configured_limit(monkeypatch):
    monkeypatch.setattr(
        "app.ai.service.settings.AI_MAX_PROMPT_LENGTH",
        5,
    )

    service = AIService(
        gateway=FakeModelGateway()
    )

    try:
        service.generate("123456")
    except ValueError as exc:
        assert str(exc) == (
            "AI prompt exceeds maximum allowed length"
        )
    else:
        raise AssertionError(
            "Expected ValueError for oversized prompt"
        )


def test_ai_service_accepts_prompt_at_configured_limit(monkeypatch):
    monkeypatch.setattr(
        "app.ai.service.settings.AI_MAX_PROMPT_LENGTH",
        5,
    )

    service = AIService(
        gateway=FakeModelGateway()
    )

    result = service.generate("12345")

    assert result == "fake response: 12345"


def test_ai_service_rejects_when_disabled(monkeypatch):
    monkeypatch.setattr(
        "app.ai.service.settings.AI_ENABLED",
        False,
    )

    service = AIService(
        gateway=FakeModelGateway()
    )

    try:
        service.generate("Hello MAJE")
    except AIServiceDisabledError as exc:
        assert str(exc) == "AI service is disabled"
    else:
        raise AssertionError(
            "Expected RuntimeError when AI service is disabled"
        )


def test_ai_service_rejects_empty_prompt():
    service = AIService(
        gateway=FakeModelGateway()
    )

    for prompt in ("", "   "):
        try:
            service.generate(prompt)
        except ValueError as exc:
            assert str(exc) == "AI prompt must not be empty"
        else:
            raise AssertionError(
                "Expected ValueError for empty prompt"
            )


def test_ai_service_preserves_valid_prompt_whitespace():
    service = AIService(
        gateway=FakeModelGateway()
    )

    result = service.generate(
        " Hello MAJE "
    )

    assert result == "fake response:  Hello MAJE "


class InvalidOutputGateway(ModelGateway):
    def generate(self, prompt: str):
        return None


def test_ai_service_rejects_invalid_gateway_output():
    service = AIService(
        gateway=InvalidOutputGateway()
    )

    try:
        service.generate("Hello MAJE")
    except AIInvalidOutputError as exc:
        assert str(exc) == "AI gateway returned invalid output"
    else:
        raise AssertionError(
            "Expected AIInvalidOutputError for invalid gateway output"
        )


class FailingGateway(ModelGateway):
    def generate(self, prompt: str) -> str:
        raise RuntimeError("SECRET_PROVIDER_ERROR")


def test_ai_service_wraps_gateway_failure():
    service = AIService(
        gateway=FailingGateway()
    )

    try:
        service.generate("Hello MAJE")
    except AIGatewayError as exc:
        assert str(exc) == "AI gateway request failed"
        assert isinstance(exc.__cause__, RuntimeError)
        assert str(exc.__cause__) == "SECRET_PROVIDER_ERROR"
    else:
        raise AssertionError(
            "Expected AIGatewayError for gateway failure"
        )
