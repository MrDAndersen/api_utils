# TODO: Update to use logging functionality from logger_utils.py
from api_utils.cache.sqlite_cache import get_sqlite_session
from sqlite_cache import get_sqlite_session
from mongo_archive import archive_response

def fetch_with_sqlite_cache(session, mongo_uri, db_name, collection, url, method="GET", params=None, headers=None, ttl_minutes=15):
    response = session.request(method, url, params=params, headers=headers)

    payload = {
        "body": response.json(),
        "status_code": response.status_code
    }

    if response.from_cache:
        print("🔄 Retrieved from SQLite cache")
    else:
        print("🌐 Fetched from live API")

        archive_response(
            mongo_uri=mongo_uri,
            db_name=db_name,
            collection=collection,
            url=url,
            method=method,
            params=params,
            headers=headers,
            response_body=payload["body"],
            status_code=payload["status_code"],
            ttl_minutes=ttl_minutes,
            source="live-api",
            tags=["sqlite", "fallback"]
        )

    return payload
