"""DynamoDB connection."""

import os
import boto3

class DynamoDBConnection:
    """Singleton class to manage DynamoDB connection."""
    _instance = None

    @classmethod
    def get_instance(cls):
        """Returns a DynamoDB resource."""
        if cls._instance is None:
            cls._instance = boto3.resource(
                "dynamodb",
                region_name=os.getenv("AWS_REGION", "ap-southeast-1")
            )
        return cls._instance