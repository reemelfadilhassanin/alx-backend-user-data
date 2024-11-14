#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, session
from flask_cors import CORS
from models.user import User

# Initialize Flask app
app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Secret key for session management (make sure this is set securely in prod)
app.secret_key = getenv("SECRET_KEY", "your_secret_key")
# Conditionally import the correct authentication class
auth = None
auth_type = getenv("AUTH_TYPE", "basic_auth")

if auth_type == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
else:
    from api.v1.auth.auth import Auth
    auth = Auth()


@app.before_request
def before_request():
    """Before request handler to filter requests."""
    if auth is None:
        return None

    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/'
    ]

    # Check if the path requires authentication
    if not auth.require_auth(request.path, excluded_paths):
        return None

    # Session-based authentication
    if request.path != '/api/v1/auth/login':  # Skip authentication for login
        user_id = session.get('user_id')  # Get user_id from session
        if user_id is None:
            abort(401, description="Unauthorized")

        # Find user from database using the user_id from session
        user = User.get(user_id)
        if user is None:
            abort(401, description="Unauthorized")

        request.current_user = user  # Set the current_user on the request


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
