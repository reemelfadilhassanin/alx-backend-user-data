#!/usr/bin/env python3
"""
Main file
"""
from db import DB
from user import User

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

my_db = DB()

# Adding users
user = my_db.add_user("test@test.com", "PwdHashed")
print(user.id)  # Output the user ID

# Finding user by email
find_user = my_db.find_user_by(email="test@test.com")
print(find_user.id)  # Output the found user's ID

# Trying to find a user that doesn't exist
try:
    find_user = my_db.find_user_by(email="test2@test.com")
    print(find_user.id)
except NoResultFound:
    print("Not found")  # Expected output since no user with this email exists

# Trying to find a user with an invalid argument
try:
    find_user = my_db.find_user_by(no_email="test@test.com")
    print(find_user.id)
except InvalidRequestError:
    print("Invalid")  # Expected output due to invalid query argument
