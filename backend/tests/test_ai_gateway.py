import pytest

from app.ai.gateway import (
    DeterministicModelGateway,
    ModelGateway,
    create_model_gateway,
)


def test_model_gateway_is_abstract():
    with pytest.raises(TypeError):
        ModelGateway()


def test_deterministic_model_gateway_returns_expected_response():
    gateway = DeterministicModelGateway()

    result = gateway.generate("Hello MAJE")

    assert result == "AI service received prompt: Hello MAJE"


def test_model_gateway_factory_uses_configured_deterministic_model(
    monkeypatch,
):
    monkeypatch.setattr(
        "app.ai.gateway.settings.AI_MODEL_NAME",
        "deterministic",
    )

    gateway = create_model_gateway()

    assert isinstance(
        gateway,
        DeterministicModelGateway,
    )


def test_model_gateway_factory_rejects_unknown_model(
    monkeypatch,
):
    monkeypatch.setattr(
        "app.ai.gateway.settings.AI_MODEL_NAME",
        "unknown-model",
    )

    with pytest.raises(
        ValueError,
        match="Unsupported AI model",
    ):
        create_model_gateway()
