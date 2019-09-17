import os
import hashlib
import binascii

from .user import User


def hash_password(password: str):
    """Hash a password for storing."""

    salt = hashlib.sha256(os.urandom(64)).hexdigest().encode('ascii')
    hashed = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 10000)
    hashed = binascii.hexlify(hashed)

    return (salt + hashed).decode('ascii')


def verify_password(password: str, stored_hash: str):
    """Verify a stored password against the provided one"""

    salt = stored_hash[:64]
    stored_password = stored_hash[64:]
    hashed = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt.encode('ascii'), 10000)
    hashed = binascii.hexlify(hashed).decode('ascii')

    return hashed == stored_password


def set_password(user: User, password: str):
    user.password = hash_password(password)
