class AIServiceError(Exception):
    """
    Base exception for controlled AI service failures.
    """


class AIServiceDisabledError(AIServiceError):
    """
    Raised when the AI service is disabled by configuration.
    """


class AIGatewayError(AIServiceError):
    """
    Raised when the model gateway fails.
    """


class AITimeoutError(AIServiceError):
    """
    Raised when an AI model or provider operation times out.
    """


class AIInvalidOutputError(AIServiceError):
    """
    Raised when the model gateway returns invalid output.
    """
