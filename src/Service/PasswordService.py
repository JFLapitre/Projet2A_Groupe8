import hashlib
import secrets
from typing import Optional

from src.DAO.userDAO import UserDAO
from src.Model.abstract_user import AbstractUser


def hash_password(password: str, salt: Optional[str] = None) -> str:
    ## TODO

    return "1234"


def create_salt() -> str:
    return secrets.token_hex(128)


def check_password_strength(password: str):
    if len(password) < 8:
        raise Exception("Password length must be at least 8 characters")


def validate_username_password(username: str, password: str, user_DAO: UserDAO) -> AbstractUser:
    user_with_username: Optional[AbstractUser] = user_DAO.get_by_username(username=username)
    ## TODO

    return user_with_username
