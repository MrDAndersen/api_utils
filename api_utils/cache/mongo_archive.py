# TODO: Add logging functionality from logger_utils.py
from pymongo import MongoClient
from datetime import datetime, UTC
from typing import Optional

def archive_response(
    mongo_uri: str,
    db_name: str,
    collection: str,
    url: str,
    method: str,
    params: dict,
    headers: dict,
    response_body: dict,
    status_code: int,
    ttl_minutes: int = 30,
    source: str = "requests-cache",
    tags: Optional[list[str]] = None
) -> None:
    """Store API response payload in MongoDB for audit clarity and TTL lineage."""
    client = MongoClient(mongo_uri)
    db = client[db_name]
    archive = db[collection]

    doc = {
        "url": url,
        "method": method,
        "params": params,
        "headers": headers,
        "response": {
            "status_code": status_code,
            "body": response_body
        },
        "timestamp": datetime.now(UTC),
        "ttl_minutes": ttl_minutes,
        "expired": False,
        "source": source,
        "tags": tags or ["archive", "cache", "api_utils"]
    }

    archive.insert_one(doc)
    