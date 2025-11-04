import hashlib
import secrets
from typing import Optional

from src.DAO.userDAO import UserDAO
from src.Model.abstract_user import AbstractUser


def hash_password(password: str, salt: Optional[str] = None) -> str:
    return hashlib.sha256((password + salt).encode()).hexdigest()


def create_salt() -> str:
    return secrets.token_hex(32)


def check_password_strength(password: str):  # à modifier à l'avenir
    if len(password) < 8:
        raise Exception("Password length must be at least 8 characters")


def validate_username_password(username: str, password: str, user_DAO: UserDAO) -> AbstractUser:
    user = user_DAO.find_user_by_username(username=username)
    if not user:
        raise ValueError("User not found.")
    if hash_password(password, user.salt) != user.password:
        raise ValueError("Incorrect password.")

    return user
