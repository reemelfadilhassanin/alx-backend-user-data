#!/usr/bin/env python3


"""
Encrypting passwords using bcrypt
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
