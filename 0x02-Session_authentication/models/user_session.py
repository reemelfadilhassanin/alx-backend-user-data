#!/usr/bin/env python3
"""
UserSession model for storing session data
"""
from models.base import Base
from datetime import datetime


class UserSession(Base):
    """Represents a user session."""

    def __init__(self, *args: list, **kwargs: dict):
        """Initializes a UserSession."""
        if kwargs:
            self.user_id = kwargs.get("user_id")
            self.session_id = kwargs.get("session_id")
            self.created_at = kwargs.get("created_at", datetime.now())
        else:
            self.user_id = args[0]
            self.session_id = args[1]
            self.created_at = datetime.now()

    def to_json(self):
        """Returns a dictionary representation of the UserSession."""
        return {
            "user_id": self.user_id,
            "session_id": self.session_id,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
