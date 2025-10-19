""" Main application entry point for AWS Lambda. """

from handlers import auth_handler, user_handler
from utils.response import build_response

ROUTES = {
    "POST /login": auth_handler.login,
    "POST /register": auth_handler.register,
    "POST /logout": auth_handler.logout,
    "GET /profile": user_handler.profile,
}

def main(event, context):
    """Main entry point for AWS Lambda."""
    http_method = event.get("httpMethod", "")
    path = event.get("path", "").rstrip("/")

    print(f"Received request: {http_method} {path}")

    if http_method == "OPTIONS":
        return build_response({}, status_code=200)

    key = f"{http_method} {path}"
    handler = ROUTES.get(key)
    if not handler:
        return build_response({"error": "Not Found"}, status_code=404)

    try:
        response = handler(event, context)
        return response
    except (ValueError, KeyError, RuntimeError) as e:
        print("Handler error:", e, flush=True)
        return build_response({"error": str(e)}, status_code=500)
