#!/usr/bin/env python3
"""
User model for user authentication service
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Create the base class for the model
Base = declarative_base()


class User(Base):
    """
    User model class for the 'users' table in the database.

    The table contains the following columns:
        - id (int): The primary key for the user record (auto-incremented).
        - email (str): The email address of the user, non-nullable.
        - hashed_password (str): The hashed password of the user, non-nullable.
        - session_id (str, nullable): A session identifier
        - reset_token (str, nullable): A reset token for the user, can be null.
    """

    __tablename__ = 'users'

    # Primary key for the user table
    id = Column(Integer, primary_key=True)

    # Email address of the user
    email = Column(String(250), nullable=False)

    # Hashed password for the user
    hashed_password = Column(String(250), nullable=False)

    # Session ID associated with the user, optional field
    session_id = Column(String(250), nullable=True)

    # Reset token for the user, optional field
    reset_token = Column(String(250), nullable=True)
