from pydantic import BaseModel

from src.Model.abstract_bundle import AbstractBundle
from src.Model.customer import Customer
from src.Model.item import Item


class Order(BaseModel):
    id: int
    customer: Customer
    adress: str
    bundles: list[AbstractBundle]
    items: list[Item]
    status: str
