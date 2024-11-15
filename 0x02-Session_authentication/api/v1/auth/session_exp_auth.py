#!/usr/bin/env python3
"""
SessionExpAuth class for session-based authentication with expiration
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """Session-based authentication with expiration support"""

    def __init__(self):
        """Initializes the SessionExpAuth class with session duration"""
        super().__init__()

        # Get the session duration from the environment variable
        try:
            self.session_duration = int(getenv("SESSION_DURATION", "0"))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create a session ID with expiration time for the given user_id."""
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        # Create session dictionary to hold user_id and expiration time
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Return user_id if session is still valid (not expired)."""
        if session_id is None:
            return None

        session_data = self.user_id_by_session_id.get(session_id)
        if session_data is None:
            return None

        # If session_duration is 0 or less, consider the session never expires
        if self.session_duration <= 0:
            return session_data["user_id"]

        # Check if the session has expired
        created_at = session_data["created_at"]
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if datetime.now() > expiration_time:
            # Session expired
            del self.user_id_by_session_id[session_id]
            return None

        # Session is still valid
        return session_data["user_id"]
