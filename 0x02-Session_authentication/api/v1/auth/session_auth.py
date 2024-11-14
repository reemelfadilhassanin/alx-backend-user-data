#!/usr/bin/env python3
"""Session Authentication Views"""
from flask import jsonify, request, make_response
from api.v1.views import app_views
from models.user import User
from api.v1.app import auth
# Import auth instance for session-based authentication


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """Handles login requests for session-based authentication."""
    # Get email and password from form data
    email = request.form.get("email")
    password = request.form.get("password")

    # Check if email or password is missing
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Retrieve the user instance based on the email
    user = User.search({"email": email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    # Check if the password is correct
    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Create a session for the user
    session_id = auth.create_session(user[0].id)

    # Prepare the response and set the session cookie
    response = make_response(jsonify(user[0].to_json()))
    session_name = getenv("SESSION_NAME", "_my_session_id")
    response.set_cookie(session_name, session_id)

    return response
