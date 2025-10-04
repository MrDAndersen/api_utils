import os
from datetime import datetime, UTC
from pymongo import MongoClient
from api_utils.cache.mongo_archive import archive_response
from dotenv import load_dotenv

# Load test-specific environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env.test"))

def test_archive_response_inserts_document():
    # Setup test config
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    db_name = "test_archive"
    collection_name = "responses"

    # Connect and clear collection
    client = MongoClient(mongo_uri)
    db = client[db_name]
    archive = db[collection_name]
    archive.delete_many({})  # Clean slate

    # Define symbolic payload
    url = "https://api.example.com/data"
    method = "GET"
    params = {"query": "value"}
    headers = {"Authorization": "Bearer test-token"}
    response_body = {"data": ["alpha", "beta"]}
    status_code = 200

    # Invoke archive ritual
    archive_response(
        mongo_uri=mongo_uri,
        db_name=db_name,
        collection=collection_name,
        url=url,
        method=method,
        params=params,
        headers=headers,
        response_body=response_body,
        status_code=status_code,
        ttl_minutes=15,
        source="test-suite",
        tags=["unit-test", "symbolic"]
    )

    # Validate document
    doc = archive.find_one({"url": url})
    assert doc is not None
    assert doc["method"] == method
    assert doc["response"]["status_code"] == status_code
    assert doc["response"]["body"] == response_body
    assert doc["expired"] is False
    assert isinstance(doc["timestamp"], datetime)
    assert doc["tags"] == ["unit-test", "symbolic"]

    client.close()
