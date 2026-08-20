from abc import ABC, abstractmethod

from app.core.config import settings


class ModelGateway(ABC):
    """
    Abstract boundary between MAJE AI orchestration
    and model provider implementations.
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate a response from the configured model provider.
        """
        raise NotImplementedError


class DeterministicModelGateway(ModelGateway):
    """
    Deterministic gateway used for development and testing.

    This implementation does not invoke an external model provider.
    """

    def generate(self, prompt: str) -> str:
        return f"AI service received prompt: {prompt}"


def create_model_gateway() -> ModelGateway:
    """
    Create the configured model gateway.

    The factory provides a controlled model-selection boundary
    without coupling AIService directly to a concrete gateway.
    """

    if settings.AI_MODEL_NAME == "deterministic":
        return DeterministicModelGateway()

    raise ValueError(
        f"Unsupported AI model: {settings.AI_MODEL_NAME}"
    )
