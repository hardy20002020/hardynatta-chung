from app.ai.gateway import (
    ModelGateway,
    create_model_gateway,
)
from app.core.config import settings
from app.ai.exceptions import (
    AIGatewayError,
    AIInvalidOutputError,
    AIServiceDisabledError,
)


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
            else create_model_gateway()
        )

    def generate(self, prompt: str) -> str:
        """
        Process an AI generation request through the
        controlled model gateway boundary.
        """

        if not settings.AI_ENABLED:
            raise AIServiceDisabledError(
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

        try:
            result = self.gateway.generate(prompt)
        except Exception as exc:
            raise AIGatewayError(
                "AI gateway request failed"
            ) from exc

        if not isinstance(result, str):
            raise AIInvalidOutputError(
                "AI gateway returned invalid output"
            )

        return result
