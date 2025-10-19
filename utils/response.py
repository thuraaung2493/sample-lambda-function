"""Utility functions for building HTTP responses."""

import os
import json
from utils.exceptions import AppError

FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")

def build_response(body=None, status_code=200, cookies=None):
    """Build an HTTP response."""
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": FRONTEND_ORIGIN,
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type,Authorization",
    }
  
    if cookies:
        headers["Set-Cookie"] = cookies
          
    return {
        "statusCode": status_code, 
        "headers": headers,
        "body": json.dumps(body or {})
    }

def make_cookie(name, value, max_age=3600, http_only=True, secure=True, same_site="Strict"):
    """Create a Set-Cookie header string."""
    cookie = f"{name}={value}; Max-Age={max_age}; Path=/; SameSite={same_site}"
    if http_only:
        cookie += "; HttpOnly"
    if secure:
        cookie += "; Secure"
    return cookie

def handle_exceptions(handler):
    """Decorator to handle exceptions and build responses."""
    def wrapper(event, context):
        try:
            return handler(event, context)
        except AppError as e:
            return build_response({"error": e.message}, e.status_code)
        except (ValueError, TypeError, AttributeError) as e:
            print("Unhandled exception:", e)
            return build_response({"error": "Internal Server Error"}, 500)
    return wrapper
