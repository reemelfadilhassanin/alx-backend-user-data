#!/usr/bin/env python3
"""
Route module for the API
"""
import logging
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin


# Conditionally import the correct authentication class
auth = None
auth_type = getenv("AUTH_TYPE", None)

if auth_type == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif auth_type == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
elif auth_type == "session_exp_auth":
    from api.v1.auth.session_exp_auth import SessionExpAuth
    auth = SessionExpAuth()
else:
    from api.v1.auth.auth import Auth
    auth = Auth()

# Setup logging
logging.basicConfig(level=logging.DEBUG)
# Set the logging level to DEBUG for detailed logs

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.before_request
def before_request():
    """Before request handler to filter requests."""
    if auth is None:
        return None

    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/', '/api/v1/forbidden/']

    # Check if the path requires authentication
    if not auth.require_auth(request.path, excluded_paths):
        logging.debug("Path does not require authentication.")
        return None

    # Validate the Authorization header
    auth_header = auth.authorization_header(request)
    if auth_header is None:
        logging.warning("No authorization header found.")
        abort(401, description="Unauthorized")
    else:
        logging.debug(f"Authorization header found: {auth_header}")

    # Check if the current user is valid
    current_user = auth.current_user(request)
    if current_user is None:
        logging.warning("User could not be authenticated.")
        abort(403, description="Forbidden")

    logging.debug(f"Authenticated user: {current_user.email}")


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
