"""Utility functions for cryptographic operations."""

import bcrypt

def hash_password(password: str) -> str:
    """Hash a password for storing."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against a given hash."""
    return bcrypt.checkpw(password.encode(), hashed.encode())
