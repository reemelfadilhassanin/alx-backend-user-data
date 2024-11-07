#!/usr/bin/env python3
"""
Main file to test password hashing.
"""

# Import the hash_password function from encrypt_password module
hash_password = __import__('encrypt_password').hash_password

# Example password to hash
password = "MyAmazingPassw0rd"

# Print the hashed password (twice to show that the salt produces a different hash each time)
print(hash_password(password))
print(hash_password(password))
