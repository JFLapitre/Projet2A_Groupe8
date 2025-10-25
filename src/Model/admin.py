from src.Model.abstract_user import AbstractUser
from src.Model.order import Order


class Admin(AbstractUser):
    adress: str = ""
    queue: list[Order] = []
