import hashlib
import re
import secrets


class PasswordService:
    """
    Service dedicated to the secure creation, hashing, and verification
    of passwords using manual salting (SHA-256).
    """

    COMMON_PASSWORDS = {"password", "12345678", "qwerty", "azerty", "admin", "motdepasse"}
    MIN_LENGTH = 8
    MIN_SCORE = 3

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
        Validates minimum strength rules for a password.
        Raises an exception with the reason for failure.
        """

        if len(password) < self.MIN_LENGTH:
            raise Exception(f"The password must be at least {self.MIN_LENGTH} characters long.")

        if password.lower() in self.COMMON_PASSWORDS:
            raise Exception("The password is one of the most commonly used passwords and is prohibited.")

        score = 0

        if re.search(r"[A-Z]", password):
            score += 1

        if re.search(r"[a-z]", password):
            score += 1

        if re.search(r"\d", password):
            score += 1

        if re.search(r"[^a-zA-Z0-9\s]", password):
            score += 1

        if score < self.MIN_SCORE:
            raise Exception(
                f"Le mot de passe doit contenir au moins {self.MIN_SCORE} des 4 types de caractères (majuscules, minuscules, chiffres, spéciaux). Score actuel : {score}/4."
            )
        return True
