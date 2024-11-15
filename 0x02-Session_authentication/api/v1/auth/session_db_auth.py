#!/usr/bin/env python3
"""
SessionDBAuth class for session authentication with database storage
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from models import storage


class SessionDBAuth(SessionExpAuth):
    """Session-based authentication with expiration and database storage."""
    
    def create_session(self, user_id=None):
        """Create a session ID and store it in the database."""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        
        # Create a new UserSession instance and store it in the database
        user_session = UserSession(user_id=user_id, session_id=session_id)
        storage.new(user_session)  # Add to the database storage
        storage.save()  # Save to the database

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Return user ID for a valid session from the database."""
        if session_id is None:
            return None

        # Find the session in the database using the session ID
        user_session = storage.get(UserSession, session_id)
        if not user_session:
            return None

        # If the session is expired, remove it and return None
        if self.session_duration > 0 and user_session.created_at + timedelta(seconds=self.session_duration) < datetime.now():
            storage.delete(user_session)
            storage.save()
            return None
        
        return user_session.user_id

    def destroy_session(self, request=None):
        """Destroy the user session based on session ID."""
        if request is None:
            return False
        
        # Get the session ID from the request cookies
        session_id = self.session_cookie(request)
        if not session_id:
            return False

        # Retrieve and delete the session from the database
        user_session = storage.get(UserSession, session_id)
        if not user_session:
            return False
        
        storage.delete(user_session)
        storage.save()

        return True
