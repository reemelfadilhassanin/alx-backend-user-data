#!/usr/bin/env python3


"""
Password encryption and validation using bcrypt
"""


import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt and return the salted hash.

    Args:
    password (str): The password to be hashed.

    Returns:
    bytes: The salted hashed password.
    """
    # Generate a salt
    salt = bcrypt.gensalt()

    # Hash the password with the generated salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates the provided password against the hashed password.

    Args:
    hashed_password (bytes): The hashed password to check against.
    password (str): The plaintext password to validate.

    Returns:
    bool: True if the password matches the hashed password, otherwise False.
    """
    # Use bcrypt's checkpw method to verify if the password matches the hash
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
