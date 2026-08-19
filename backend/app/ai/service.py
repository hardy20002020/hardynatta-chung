from app.ai.gateway import (
    DeterministicModelGateway,
    ModelGateway,
)
from app.core.config import settings


class AIService:
    """
    Controlled AI service boundary.

    AIService owns application-level AI orchestration while
    ModelGateway owns model-provider interaction.
    """

    def __init__(
        self,
        gateway: ModelGateway | None = None,
    ):
        self.gateway = (
            gateway
            if gateway is not None
            else DeterministicModelGateway()
        )

    def generate(self, prompt: str) -> str:
        """
        Process an AI generation request through the
        controlled model gateway boundary.
        """

        if not settings.AI_ENABLED:
            raise RuntimeError(
                "AI service is disabled"
            )

        if not prompt.strip():
            raise ValueError(
                "AI prompt must not be empty"
            )

        if len(prompt) > settings.AI_MAX_PROMPT_LENGTH:
            raise ValueError(
                "AI prompt exceeds maximum allowed length"
            )

        return self.gateway.generate(prompt)
