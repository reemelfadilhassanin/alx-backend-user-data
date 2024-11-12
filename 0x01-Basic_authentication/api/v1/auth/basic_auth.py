#!/usr/bin/env python3
"""Basic authentication module for the API.
"""
import re
from .auth import Auth


class BasicAuth(Auth):
    """Basic authentication class.
    This class will handle all Basic Authentication logic for the API.
    It extends the Auth class and implements methods to:
      - Extract the Base64 part of the Authorization header.
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extracts the Base64 part of the Authorization

        Args:
            authorization_header (str): The full Authorization header

        Returns:
            str: The Base64 part of the header if valid, None otherwise.
        """
        # Check if authorization_header is None or not a string
        if not isinstance(authorization_header, str):
            return None

        # Check if the string starts with 'Basic ' (with a space at the end)
        if not authorization_header.startswith("Basic "):
            return None

        # Return the Base64 part (after 'Basic ')
        return authorization_header[6:]
