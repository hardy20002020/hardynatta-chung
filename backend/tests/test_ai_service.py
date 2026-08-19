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
