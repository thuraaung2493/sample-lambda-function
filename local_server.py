"""Local server to simulate AWS Lambda environment using Flask."""

import os
import json
from flask import Flask, request, make_response
from app import main as lambda_handler

# Enable in-memory DB for local testing
os.environ["USE_MEMORY_DB"] = "1"

app = Flask(__name__)

def lambda_event_from_request(req):
    """Convert Flask request to Lambda event format."""
    return {
        "httpMethod": req.method,
        "path": req.path,
        "headers": dict(req.headers),
        "body": req.get_data(as_text=True)
    }

@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "OPTIONS"])
@app.route("/<path:path>", methods=["GET", "POST", "OPTIONS"])
def handler(path):
    """Handle incoming HTTP requests and route to Lambda handler."""
    event = lambda_event_from_request(request)
    print(f"Received event: {event}")
    # Handle OPTIONS preflight for CORS
    if request.method == "OPTIONS":
        resp = make_response("", 200)
        resp.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
        resp.headers["Access-Control-Allow-Credentials"] = "true"
        resp.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
        resp.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
        return resp

    # Call Lambda handler
    response = lambda_handler(event, None)
    body = json.loads(response.get("body", "{}"))
    status_code = response.get("statusCode", 200)

    resp = make_response(body, status_code)
    for k, v in response.get("headers", {}).items():
        resp.headers[k] = v
    return resp

if __name__ == "__main__":
    app.run(port=4000, debug=True)
