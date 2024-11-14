#!/usr/bin/env python3
"""
SessionAuth class for session-based authentication
"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """Session-based authentication class.

    This class implements session-based authentication.
    It allows the creation of
    a session ID for a given user_id and stores them in memory.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a session ID for the given user_id.

        Args:
            user_id (str): The user_id for which the session ID is created.

        Returns:
            str: The generated session ID, or None if user_id is invalid.
        """
        # Check if user_id is valid
        if user_id is None or not isinstance(user_id, str):
            return None

        # Generate a new session ID using uuid4
        session_id = str(uuid.uuid4())

        # Store the session_id with user_id in the class attribute
        self.user_id_by_session_id[session_id] = user_id

        return session_id
