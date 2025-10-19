"""Data Transfer Objects for User operations."""
from dataclasses import dataclass

@dataclass
class RegisterInputDTO:
    """Data Transfer Object for user registration."""
    email: str
    password: str
    name: str

@dataclass
class LoginInputDTO:
    """Data Transfer Object for user login."""
    email: str
    password: str

@dataclass
class UserOutputDTO:
    """Data Transfer Object for user output."""
    email: str
    name: str

    @classmethod
    def from_user(cls, user):
        """Create UserOutputDTO from a user model instance."""
        return cls(email=user.email, name=user.name)
