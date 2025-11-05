from typing import Optional

from src.Model.abstract_user import AbstractUser
from src.Model.address import Address
from src.Model.order import Order


class Admin(AbstractUser):
    name: str = ""
    adress: Optional[Address] = None
    queue: list[Order] = []
    phone_number: Optional[str] = None
