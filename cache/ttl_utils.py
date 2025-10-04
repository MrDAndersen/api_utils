from datetime import datetime, timedelta

def is_expired(timestamp: datetime, ttl_minutes: int) -> bool:
    """Check if a cached item is expired based on TTL."""
    return datetime.utcnow() > timestamp + timedelta(minutes=ttl_minutes)
