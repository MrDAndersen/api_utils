from requests_cache import CachedSession
from datetime import timedelta

def get_sqlite_session(ttl_minutes: int = 30) -> CachedSession:
    """Create a requests session with SQLite-based TTL cache."""
    return CachedSession(
        cache_name="api_cache",
        backend="sqlite",
        expire_after=timedelta(minutes=ttl_minutes),
        allowable_methods=["GET", "POST"],
        stale_if_error=True
    )
