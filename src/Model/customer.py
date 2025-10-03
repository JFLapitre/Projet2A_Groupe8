from abstract_user.py import AbstractUser
from order.py import Order


class Customer(AbstractUser):
    current_order: Order
