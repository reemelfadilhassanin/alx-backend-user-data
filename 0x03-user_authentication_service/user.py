#!/usr/bin/env python3
"""
User model for user authentication service
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    User model class for the 'users' table.

    Attributes:
        id (int): The primary key for the user record.
        email (str): The email of the user, non-nullable.
        hashed_password (str): The hashed password user
        session_id (str, nullable): A session identifier
        reset_token (str, nullable): A reset token for the user
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
