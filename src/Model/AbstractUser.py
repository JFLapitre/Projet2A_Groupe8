from abc import ABC

from pydantic import BaseModel


class AbstractUser(BaseModel, ABC):
    id: int
    name: str
    password: str
    mail: str

