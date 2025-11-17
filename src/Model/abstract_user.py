from abc import ABC
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AbstractUser(BaseModel, ABC):
    """
    Abstract base class for all bundles

    Attributes:
        id_user (Optional[int]): Unique identifier for the user.
        username (str): Username for authentification.
        hash_password (str): Hash password for authentification.
        salt (str): Salt for authentification with hash password.
        sign_up_date (Optional[datetime]): Date of last authentification.
    """
    id_user: Optional[int] = None
    username: str
    hash_password: str
    salt: str
    sign_up_date: Optional[datetime] = None
