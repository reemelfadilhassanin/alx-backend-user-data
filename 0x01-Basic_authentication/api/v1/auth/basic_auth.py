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
                                           base64_authorizat: str) -> str:
        """Decodes a base64-encoded authorization header.

        Args:
            base64_authorization_header (str): The Base64 authorization string.

        Returns:
            str: The decoded value as a UTF-8 string if valid, None otherwise.
        """
        # Check if base64_authorization_header is None or not a string
        if not isinstance(base64_authorizat, str):
            return None

        # Try to decode the Base64 string
        try:
            decoded_bytes = base64.b64decode(base64_authorizat,
                                             validate=True)
            return decoded_bytes.decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            # If decoding fails, return None
            return None
