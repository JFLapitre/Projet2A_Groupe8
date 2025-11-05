from abc import ABC
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AbstractUser(BaseModel, ABC):
    id_user: Optional[int] = None
    username: str
    hash_password: str
    salt: str
    sign_up_date: Optional[datetime] = None
