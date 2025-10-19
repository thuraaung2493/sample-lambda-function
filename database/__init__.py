"""Database connection manager."""

import os
from .in_memory import MemoryDBConnection
from .dynamo import DynamoDBConnection

def get_db():
    """Return either real DynamoDB or in-memory DB based on env."""
    use_memory = os.getenv("USE_MEMORY_DB", "0") == "1"
    if use_memory:
        return MemoryDBConnection.get_instance()
    return DynamoDBConnection.get_instance()
