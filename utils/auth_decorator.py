"""Utility functions for handling authentication and authorization."""

from functools import wraps
from utils.jwt_utils import verify_token
from utils.exceptions import UnauthorizedError

def require_auth(handler):
    """Decorator to require authentication for a handler."""
    @wraps(handler)
    def wrapper(event, context):
        headers = event.get("headers", {}) or {}
        cookies = headers.get("cookie", "")
        token = None
        for part in cookies.split(";"):
            k, _, v = part.strip().partition("=")
            if k == "access_token":
                token = v
                break
        if not token:
            raise UnauthorizedError("Missing authentication token")
        payload = verify_token(token)
        if not payload:
            raise UnauthorizedError("Invalid or expired token")
        event["auth"] = payload
        return handler(event, context)
    return wrapper
