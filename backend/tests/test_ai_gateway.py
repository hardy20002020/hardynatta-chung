import pytest

from app.ai.gateway import (
    DeterministicModelGateway,
    ModelGateway,
)


def test_model_gateway_is_abstract():
    with pytest.raises(TypeError):
        ModelGateway()


def test_deterministic_model_gateway_returns_expected_response():
    gateway = DeterministicModelGateway()

    result = gateway.generate("Hello MAJE")

    assert result == "AI service received prompt: Hello MAJE"
