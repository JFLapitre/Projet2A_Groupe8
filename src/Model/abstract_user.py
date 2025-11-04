from abc import ABC
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AbstractUser(BaseModel, ABC):
    id_user: int
    username: str
    password: str
    sign_up_date: Optional[datetime] = None
