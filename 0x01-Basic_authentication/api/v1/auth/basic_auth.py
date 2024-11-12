#!/usr/bin/env python3
"""Basic authentication module for the API.
"""
import base64
import binascii
from .auth import Auth


class BasicAuth(Auth):
    """Basic authentication class.
    This class handles all Basic Authentication logic for the API.
    It extends the Auth class and implements methods to:
      - Extract the Base64 part of the Authorization header.
      - Decode the Base64 part to get the user credentials.
    """

    def decode_base64_authorization_header(self,
                                           base64_authorization: str) -> str:
        """Decodes a base64-encoded authorization header.

        Args:
            base64_authorization_header (str): The Base64 authorization string.

        Returns:
            str: The decoded value as a UTF-8 string if valid, None otherwise.
        """
        # Check if base64_authorization_header is None or not a string
        if not isinstance(base64_authorization, str):
            return None

        # Try to decode the Base64 string
        try:
            decoded_bytes = base64.b64decode(base64_authorization,
                                             validate=True)
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
