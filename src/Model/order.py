from abstract_bundle.py import AbstractBundle
from customer.py import Customer
from pydantic import BaseModel


class Order(BaseModel):
    id: int
    customer: Customer
    adress: str
    bundles: list[AbstractBundle]
    status: str
