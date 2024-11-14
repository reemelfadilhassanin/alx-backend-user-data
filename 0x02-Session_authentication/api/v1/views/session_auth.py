#!/usr/bin/env python3
"""
Session Authentication views
"""
from flask import request, jsonify, abort, make_response
from api.v1.views import app_views
from models.user import User
from api.v1.app import auth  # Import auth here to avoid circular imports

@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """POST /api/v1/auth_session/login"""
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if email or password is missing
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Search for the user by email
    user = User.search({"email": email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    user = user[0]  # Assuming `User.search()` returns a list

    # Check if the password is correct
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Create session
    session_id = auth.create_session(user.id)

    # Create a response with user data and set the session ID in the cookie
    response = make_response(jsonify(user.to_json()))
    response.set_cookie(auth.session_name(), session_id)

    return response


@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """DELETE /api/v1/auth_session/logout - Logs out the current user"""
    
    # Attempt to destroy the session
    if not auth.destroy_session(request):
        abort(404)  # Session not found, so return 404

    # If session is destroyed successfully, return an empty JSON response with status 200
    return jsonify({}), 200
