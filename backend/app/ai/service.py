from app.ai.gateway import (
    DeterministicModelGateway,
    ModelGateway,
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
            else DeterministicModelGateway()
        )

    def generate(self, prompt: str) -> str:
        """
        Process an AI generation request through the
        controlled model gateway boundary.
        """

        return self.gateway.generate(prompt)
