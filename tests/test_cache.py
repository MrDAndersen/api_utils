import pytest
from datetime import datetime, timedelta, UTC
from api_utils.cache.sqlite_cache import get_sqlite_session
from api_utils.cache.ttl_utils import is_expired

def test_sqlite_session_creation():
    session = get_sqlite_session(ttl_minutes=15)
    assert session is not None
    assert session.cache is not None
    assert session.expire_after.total_seconds() == 900  # 15 minutes

def test_ttl_expiry_logic():
    now = datetime.now(UTC)
    expired = is_expired(now - timedelta(minutes=20), ttl_minutes=15)
    not_expired = is_expired(now - timedelta(minutes=10), ttl_minutes=15)
    assert expired is True
    assert not_expired is False