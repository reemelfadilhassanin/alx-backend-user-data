#!/usr/bin/env python3
"""Basic authentication module for the API.
"""
import base64
import binascii
from .auth import Auth
from models.user import User


class BasicAuth(Auth):
    """Basic authentication class.
    This class handles all Basic Authentication logic for the API.
    It extends the Auth class and implements methods to:
      - Extract the Base64 part of the Authorization header.
      - Decode the Base64 part to get the user credentials.
      - Retrieve the user based on credentials.
    """

    def decode_base64_authorization_header(self, base64_: str) -> str:
        """Decodes a base64-encoded authorization header.

        Args:
            base64_authorization_header (str): The Base64 authorization string.

        Returns:
            str: The decoded value as a UTF-8 string if valid, None otherwise.
        """
        # Check if base64_authorization_header is None or not a string
        if not isinstance(base64_, str):
            return None

        # Try to decode the Base64 string
        try:
            decoded_bytes = base64.b64decode(base64_, validate=True)
            return decoded_bytes.decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            # If decoding fails, return None
            return None

    def extract_user_credentials(self, decoded_base64_: str) -> (str, str):
        """Extracts user credentials (email and password)

        Args:
            decoded_base64_authorization_header (str)

        Returns:
            tuple: A tuple containing the email and password
        """
        # Check if decoded_base64_authorization_header is None or not a string
        if not isinstance(decoded_base64_, str):
            return None, None

        # Check if the string contains ':'
        if ':' not in decoded_base64_:
            return None, None

        # Split the string into email and password
        email, password = decoded_base64_.split(':', 1)
        return email, password

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> 'User':
        """Returns a User instance based on email and password.

        Args:
            user_email (str): The email of the user.
            user_pwd (str): The password of the user.

        Returns:
            User: The user instance if valid credentials are found
        """
        # Check if user_email and user_pwd are strings
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None

        # Use the search method to find users by email
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        # If no user is found with the given email, return None
        if len(users) == 0:
            return None

        # Check if the provided password matches the user's password
        user = users[0]
        if user.is_valid_password(user_pwd):
            return user

        return None

    def current_user(self, request=None) -> 'User':
        """Retrieve the current user based on the Authorization header.

        Args:
            request (flask.Request, optional): The Flask request object.

        Returns:
            User: The user instance if credentials are valid, None otherwise.
        """
        # Check if request is provided
        if not request:
            return None

        # Retrieve the authorization header from the request
        authorization_header = request.headers.get('Authorization')

        # Check if the header is present and starts with 'Basic'
        if not authorization_header or not authorization_header.startswith(
            "Basic "):
            return None

        # Extract the Base64 part of the authorization header
        base64_part = self.extract_base64_authorization_header(
            authorization_header)

        # Decode the Base64 part into a string
        decoded = self.decode_base64_authorization_header(base64_part)

        # Extract the email and password from the decoded string
        email, password = self.extract_user_credentials(decoded)

        # Return the user object based on credentials
        return self.user_object_from_credentials(email, password)
