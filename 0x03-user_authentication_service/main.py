#!/usr/bin/env python3
"""
Main file to test User model
"""

from user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Setup in-memory database for testing
engine = create_engine('sqlite:///:memory:', echo=True)

# Create the table in the in-memory database
User.__table__.create(engine)

# Inspect the table columns
print(User.__tablename__)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Create a new user
new_user = User(email="test@example.com", hashed_password="hashed_password")
session.add(new_user)
session.commit()

# Print all users
for user in session.query(User).all():
    print(user.id, user.email)

