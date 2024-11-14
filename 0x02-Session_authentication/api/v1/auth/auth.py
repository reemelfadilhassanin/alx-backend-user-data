#!/usr/bin/env python3
""" Auth class for API Authentication
"""
from typing import List
from flask import request
from os import getenv


class Auth:
    """ Auth class to manage API authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines whether authentication is required for the given path.
        Returns True if the path is not in the excluded_paths list.
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Remove trailing slashes for slash tolerance
        path = path.rstrip("/")
        for excluded in excluded_paths:
            # Remove trailing slashes for slash tolerance on excluded paths
            excluded = excluded.rstrip("/")
            if path == excluded:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns the Authorization header from the Flask request object.
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None):
        """
        Returns the current user from the request.
        For now, it returns None, as no user authentication is implemented.
        """
        return None

    def session_cookie(self, request=None):
        """
        Returns the session cookie value from the request.

        Args:
            request (flask.Request): The Flask request object.

        Returns:
            str: The value of the session cookie if found, or None if not.
        """
        # Return None if request is None
        if request is None:
            return None

        # Get the cookie name from the environment variable 'SESSION_NAME'
        session_name = getenv("SESSION_NAME", "_my_session_id")

        # Get the session ID from the cookies using the session name
        return request.cookies.get(session_name, None)
