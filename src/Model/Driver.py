from AbstractUser.py import AbstractUser
from Delivery.py import Delivery


class Driver(AbstractUser):
    deliveries: list[Delivery]
