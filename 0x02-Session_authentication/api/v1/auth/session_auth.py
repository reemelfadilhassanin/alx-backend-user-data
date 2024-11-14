#!/usr/bin/env python3
"""
SessionAuth class for session-based authentication
"""
from api.v1.auth.auth import Auth
import uuid

class SessionAuth(Auth):
    """Session-based authentication class.

    This class implements session-based authentication.
    It allows the creation of a session ID for a given user_id and stores them in memory.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a session ID for the given user_id.

        Args:
            user_id (str): The user_id for which the session ID is created.

        Returns:
            str: The generated session ID, or None if user_id is invalid.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return the User ID based on the Session ID.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            str: The user_id associated with the session_id, or None if not found.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id, None)

    def destroy_session(self, request=None) -> bool:
        """Destroy the session for the current user.

        Args:
            request (flask.Request): The request object.

        Returns:
            bool: True if session was successfully destroyed, False otherwise.
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        # Delete the session from the dictionary
        del self.user_id_by_session_id[session_id]
        return True
