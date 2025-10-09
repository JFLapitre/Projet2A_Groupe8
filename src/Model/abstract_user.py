from abc import ABC

from pydantic import BaseModel


class AbstractUser(BaseModel, ABC):
    id_user: int
    username: str
    password: str
    sign_up_date: str
