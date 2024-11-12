#!/usr/bin/env python3
""" Auth class for API Authentication
"""
from typing import List
from flask import request


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
        Returns the Authorization header
        For now, it returns None a
        """
        return None

    def current_user(self, request=None):
        """
        Returns the current user from the request.
        For now, it returns None, as no user authentication is implemented.
        """
        return None
