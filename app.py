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
    path = event.get("path", "")

    if http_method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "http://localhost:5173",
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type,Authorization",
            },
            "body": "",
        }

    key = f"{http_method} {path}"
    print(f"Routing request: {key}")
    handler = ROUTES.get(key)
    if not handler:
        return build_response({"error": "Not Found"}, status_code=404)

    return handler(event, context)
