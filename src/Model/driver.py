from abstract_user.py import AbstractUser
from delivery.py import Delivery


class Driver(AbstractUser):
    deliveries: list[Delivery]
