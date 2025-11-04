import hashlib
import secrets


class PasswordService:
    """
    Service dedicated to the secure creation, hashing, and verification
    of passwords using manual salting (SHA-256), compatible with
    your database schema (separate salt column).
    """

    def __init__(self):
        pass

    def create_salt(self) -> str:
        """
        Creates a secure, random salt string.
        (Using 32 bytes/64 hex characters, matching the common storage size.)
        """
        return secrets.token_hex(32)

    def hash_password(self, password: str, salt: str = None) -> str:
        """
        Hashes a plain text password combined with a salt using SHA-256.
        The salt parameter is mandatory for secure hashing.
        """
        if not salt:
            raise ValueError("Salt must be provided for secure hashing.")

        return hashlib.sha256((password + salt).encode()).hexdigest()

    def check_password_strength(self, password: str):
        """
        Validates minimum password strength rules (e.g., minimum length).
        (Functionality to be expanded later.)
        """
        if len(password) < 8:
            raise Exception("Password length must be at least 8 characters")
