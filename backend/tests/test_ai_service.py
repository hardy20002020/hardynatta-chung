from app.ai.gateway import ModelGateway
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
    except RuntimeError as exc:
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
