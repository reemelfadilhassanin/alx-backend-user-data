#!/usr/bin/env python3
""" Auth class for API Authentication
"""
from typing import List
from flask import request


class Auth:
    """ Auth class to manage API authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines whether authentication is require
        For now, it always returns False
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Returns the Authorization header
        For now, it returns None
        """
        return None

    def current_user(self, request=None):
        """
        Returns the current user from the request.
        For now, it returns None, as no user authentication is implemented.
        """
        return None
