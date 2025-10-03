from AbstractUser.py import AbstractUser
from Order.py import Order


class Customer(AbstractUser):
    current_order: Order
