#!/usr/bin/env python3
"""
SessionAuth class for session-based authentication
"""
from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """Session-based authentication class.

    This class implements session-based authentication.
    It allows the creation of a session ID for
    a given user_id and stores them in memory.
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
        # Generate a unique session ID
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return the User ID based on the Session ID.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            str: The user_id associated with the session_id, or None.
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

        # Get the session ID from the cookie
        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        # Get the user ID associated with the session ID
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        # Delete the session from the dictionary
        del self.user_id_by_session_id[session_id]
        return True

    def current_user(self, request=None) -> 'User':
        """Retrieve the current user based on the session cookie.

        Args:
            request (flask.Request, optional): The Flask request object.

        Returns:
            User: The user instance if credentials are valid, None otherwise.
        """
        if not request:
            return None

        # Retrieve the session ID from the request cookies
        session_id = self.session_cookie(request)
        if not session_id:
            return None

        # Get the user ID from the session ID
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return None

        # Retrieve the user based on the user ID
        try:
            user = User.get(user_id)
            # Assuming User.get() fetches the user by user_id
        except Exception:
            return None

        return user

    def session_cookie(self, request=None):
        """Retrieve the session cookie from the request."""
        if not request:
            return None
        return request.cookies.get(self.session_name())

    def session_name(self):
        """Return the name of the session cookie."""
        return "_my_session_id"  # Customize this name as needed
