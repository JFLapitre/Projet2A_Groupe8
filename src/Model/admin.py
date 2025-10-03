from abstract_user.py import AbstractUser
from order.py import Order


class Admin(AbstractUser):
    adress: str
    queue: list[Order]
