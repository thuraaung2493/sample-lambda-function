"""Utility functions for JWT token generation and verification."""

import os
import datetime
import jwt

SECRET_KEY = os.getenv("JWT_SECRET", "supersecretkey")
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60

def generate_token(payload: dict):
    """Generate a JWT token with an expiration time."""
    exp = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    payload["exp"] = exp
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    """Verify a JWT token and return the payload if valid."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
