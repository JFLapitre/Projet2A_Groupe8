from AbstractBundle.py import AbstractBundle
from Customer.py import Customer
from pydantic import BaseModel


class Order(BaseModel):
    id: int
    customer: Customer
    adress: str
    bundles: list[AbstractBundle]
    status: str
