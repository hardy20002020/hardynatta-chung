from abc import ABC, abstractmethod


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
