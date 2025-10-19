""" User profile handler. """

from utils.response import handle_exceptions, build_response
from utils.auth_decorator import require_auth

@handle_exceptions
@require_auth
def profile(event, _context):
    """Get the authenticated user's profile."""
    user_info = event["auth"]
    return build_response({"email": user_info["email"], "name": user_info.get("name")})
