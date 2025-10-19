"""User model."""

from dataclasses import dataclass

@dataclass
class User:
    """User model."""
    email: str
    name: str
    password_hash: str
    created_at: int

    @classmethod
    def from_dict(cls, data: dict):
        """Create a User instance from a dictionary."""
        return cls(
            email=data.get("email"),
            name=data.get("name"),
            password_hash=data.get("password_hash"),
            created_at=data.get("created_at"),
        )

    def to_dict(self):
        """Convert User instance to a dictionary."""
        return {
            "email": self.email,
            "name": self.name,
            "password_hash": self.password_hash,
            "created_at": self.created_at,
        }
