from datetime import datetime, timezone


def utcnow(ctx=None) -> datetime:
    """
    Return the current UTC timestamp as a naive datetime
    for database storage.
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)
