from pymongo import MongoClient
from datetime import datetime

def archive_response(mongo_uri: str, db_name: str, collection: str, payload: dict) -> None:
    """Store API response payload in MongoDB for audit clarity."""
    client = MongoClient(mongo_uri)
    db = client[db_name]
    archive = db[collection]
    archive.insert_one({
        "timestamp": datetime.utcnow(),
        "payload": payload
    })
