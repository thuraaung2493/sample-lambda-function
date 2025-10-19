"""Authentication service for user login and registration."""

import time
from utils import crypto, jwt_utils
from utils.exceptions import UnauthorizedError, ValidationError
from repositories.user_repository import UserRepository
from dtos.user_dto import RegisterInputDTO, LoginInputDTO, UserOutputDTO
from models.user import User

user_repo = UserRepository()

def login_user(dto: LoginInputDTO):
    """Login a user and return a JWT token."""

    user_data = user_repo.get_by_email(dto.email)
    if not user_data:
        raise UnauthorizedError("Invalid credentials")
    
    user = User.from_dict(user_data)
    if not crypto.verify_password(dto.password, user.password_hash):
        raise UnauthorizedError("Invalid credentials")

    token = jwt_utils.generate_token({"email": user.email, "name": user.name})
    return {"token": token, "user": UserOutputDTO.from_user(user).__dict__}

def register_user(dto: RegisterInputDTO):
    """Register a new user and return a JWT token."""

    if user_repo.get_by_email(dto.email):
        raise ValidationError("User already exists")

    hashed = crypto.hash_password(dto.password)
    user = User(email=dto.email, name=dto.name, password_hash=hashed, created_at=int(time.time()))
    user_repo.create_user(**user.to_dict())

    token = jwt_utils.generate_token({"email": user.email, "name": user.name})
    return {"token": token, "user": UserOutputDTO.from_user(user).__dict__}
