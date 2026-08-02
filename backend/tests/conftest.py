import pytest

from app.core.rate_limit import limiter


@pytest.fixture(autouse=True)
def reset_rate_limiter():
    """
    Keep rate-limited tests isolated from each other.

    The production limiter remains enabled. Only its
    in-memory test counters are reset between tests.
    """

    limiter.reset()

    yield

    limiter.reset()
