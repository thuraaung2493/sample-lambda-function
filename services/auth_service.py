"""Authentication service for user login and registration."""

import time
from utils import crypto, jwt_utils
from utils.exceptions import UnauthorizedError, ValidationError
from repositories.user_repository import UserRepository

user_repo = UserRepository()

def login_user(email: str, password: str):
    """Login a user and return a JWT token."""

    if not email or not password:
        raise ValidationError("Email and password are required")

    user = user_repo.get_by_email(email)
    if not user or not crypto.verify_password(password, user["password_hash"]):
        raise UnauthorizedError("Invalid credentials")

    token = jwt_utils.generate_token({"email": email, "name": user.get("name")})
    return {"token": token, "user": {"email": email, "name": user.get("name")}}

def register_user(email: str, password: str, name: str):
    """Register a new user and return a JWT token."""

    if user_repo.get_by_email(email):
        raise ValidationError("User already exists")

    hashed = crypto.hash_password(password)
    created_at = int(time.time())
    user_repo.create_user(email, hashed, name, created_at)

    token = jwt_utils.generate_token({"email": email, "name": name})
    return {"token": token, "user": {"email": email, "name": name}}
