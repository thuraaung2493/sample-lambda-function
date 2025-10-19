"""Exception classes for application-specific errors."""

class AppError(Exception):
    """Base class for all application errors."""
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class NotFoundError(AppError):
    """Custom error for resource not found."""
    def __init__(self, message="Resource not found"):
        super().__init__(message, 404)

class UnauthorizedError(AppError):
    """Custom error for unauthorized access."""
    def __init__(self, message="Unauthorized"):
        super().__init__(message, 401)

class ValidationError(AppError):
    """Custom error for validation failures."""
    def __init__(self, message="Validation error"):
        super().__init__(message, 422)
