""" Authentication handlers for login, registration, and logout. """

import json
from dtos.user_dto import LoginInputDTO, RegisterInputDTO
from utils.response import handle_exceptions, build_response, make_cookie
from services.auth_service import login_user, register_user

@handle_exceptions
def login(event, _context):
    """Login a user and return a JWT token."""
    body = json.loads(event.get("body") or "{}")
    dto = LoginInputDTO(**body)
    result = login_user(dto)
    cookie = make_cookie("access_token", result["token"], max_age=3600)
    return build_response({"user": result["user"]}, cookies=cookie)

@handle_exceptions
def register(event, _context):
    """Register a new user and return a JWT token."""
    body = json.loads(event.get("body") or "{}")
    dto = RegisterInputDTO(**body)
    result = register_user(dto)
    cookie = make_cookie("access_token", result["token"], max_age=3600)
    print(f"Register response cookie: {cookie}")
    return build_response({"user": result["user"]}, cookies=cookie)

@handle_exceptions
def logout(_event, _context):
    """Logout a user by clearing the authentication cookie."""
    cookie = make_cookie("access_token", "", max_age=0)
    return build_response({"message": "Logged out"}, cookies=cookie)
