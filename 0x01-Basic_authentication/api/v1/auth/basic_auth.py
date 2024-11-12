#!/usr/bin/env python3
""" BasicAuth class to manage basic authentication.
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ Basic Authentication class. Inherit from Auth class.
        This class will handle Basic Auth-related tasks
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Extracts the base64 part of the Authorization header for Basic Auth.

        Args:
            authorization_header (str): The full Authorization header.

        Returns:
            str: The base64 part after 'Basic'
        """
        # Check if authorization_header is None or not a string
        if authorization_header is None or
        not isinstance(authorization_header, str):
            return None

        # Check if the string starts with 'Basic '
        if not authorization_header.startswith("Basic "):
            return None

        # Return the base64 part (after 'Basic ')
        return authorization_header[6:]
