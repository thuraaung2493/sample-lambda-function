"""Repository for user operations."""

from database import get_db

USERS_TABLE = "Users"

class UserRepository:
    """Repository for user operations."""
    def __init__(self):
        self.table = get_db().Table(USERS_TABLE)

    def get_by_email(self, email: str):
        """Get user by email."""
        res = self.table.get_item({"email": email})
        return res.get("Item")

    def create_user(self, email: str, password_hash: str, name: str, created_at: int):
        """Create a new user."""
        item = {
            "email": email,
            "password_hash": password_hash,
            "name": name,
            "created_at": created_at
        }
        self.table.put_item(item)
        return item

    def update_user(self, email: str, updates: dict):
        """Update user information."""
        if not updates:
            return self.get_by_email(email)

        # Simple SET expression for MemoryDB and DynamoDB
        update_expr = "SET " + ", ".join([f"#{k} = :{k}" for k in updates])
        expr_attr_names = {f"#{k}": k for k in updates}
        expr_attr_values = {f":{k}": v for k, v in updates.items()}

        self.table.update_item(
            Key={"email": email},
            UpdateExpression=update_expr,
            ExpressionAttributeNames=expr_attr_names,
            ExpressionAttributeValues=expr_attr_values
        )
        return self.get_by_email(email)
