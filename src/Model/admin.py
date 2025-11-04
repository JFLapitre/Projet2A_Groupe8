from typing import Optional

from src.Model.abstract_user import AbstractUser
from src.Model.order import Order


class Admin(AbstractUser):
    name: str = ""
    adress: str = ""
    queue: list[Order] = []
    phone_number: Optional[str] = None
