from AbstractUser.py import AbstractUser
from Order.py import Order


class Admin(AbstractUser):
    adress: str
    queue: list[Order]
