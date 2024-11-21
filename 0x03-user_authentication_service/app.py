#!/usr/bin/env python3
"""
Flask app to manage user authentication,
sessions, and password reset
"""
from auth import Auth
from flask import Flask, abort, jsonify, request, redirect, url_for

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
AUTH = Auth()


@app.route("/")
def home() -> str:
    """ Home endpoint
        This route returns a welcome message
        Return:
            - JSON message
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/sessions", methods=["POST"])
def login():
    """ Login endpoint
        This route allows users to log in
        Form fields:
            - email: User's email address
            - password: User's password
        Return:
            - JSON with the user’s email and a success message
            if credentials are valid
            - 401 if credentials are invalid
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"])
def logout():
    """ Logout endpoint
        This route logs out the user
        Return:
            - Redirects to the home
            - 403 if no valid session is found
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect(url_for("home"))


@app.route("/users", methods=["POST"])
def users():
    """ New user signup endpoint
        This route allows a new user to register
        Form fields:
            - email: User's email address
            - password: User's password
        Return:
            - JSON message with the user's email
            - 400 if the email is already registered
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/profile")
def profile() -> str:
    """ User profile endpoint
        This route returns the profile of
        the currently logged-in user.
        Return:
            - JSON with the user's email
            - 403 if the session is not valid or
            not linked to any user
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    return jsonify({"email": user.email})


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token() -> str:
    """ Reset password token endpoint
        This route allows the user to request
        a password reset by providing their email.
        Form fields:
            - email: User's email address
        Return:
            - JSON with the user's email and a
            reset token if the email is valid
            - 403 if the email is not associated with any user
    """
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "reset_token": reset_token})


@app.route("/reset_password", methods=["PUT"])
def update_password():
    """ Password update endpoint
        This route allows a user to update their password
        Form fields:
            - email: User's email address
            - reset_token: Token received
            - new_password: New password to be set
        Return:
            - JSON message with the user's email
            - 403 if the reset token is not valid
    """
    email = request.form.get("email")
    new_password = request.form.get("new_password")
    reset_token = request.form.get("reset_token")

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
