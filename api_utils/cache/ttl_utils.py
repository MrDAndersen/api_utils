from datetime import datetime, timedelta, UTC

def is_expired(timestamp: datetime, ttl_minutes: int) -> bool:
    """Check if a cached item is expired based on TTL."""
    return datetime.now(UTC) > timestamp + timedelta(minutes=ttl_minutes)
