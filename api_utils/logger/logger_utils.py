# TODO: Create tests for this module

import logging
from logging.handlers import RotatingFileHandler
from pymongo import MongoClient
from datetime import datetime, UTC

def get_logger(name="api_utils", level=logging.INFO, log_file="api_utils.log"):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        ))

        # Rotating file handler
        file_handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=5)
        file_handler.setFormatter(logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        ))

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger


def log_to_mongo(mongo_uri, db_name, collection, level, message, tags=None, source="logger_utils"):
    client = MongoClient(mongo_uri)
    db = client[db_name]
    logs = db[collection]

    log_entry = {
        "timestamp": datetime.now(UTC),
        "level": level,
        "message": message,
        "tags": tags or [],
        "source": source
    }

    logs.insert_one(log_entry)
