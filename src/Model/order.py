from pydantic import BaseModel

from src.Model.abstract_bundle import AbstractBundle
from src.Model.address import Address
from src.Model.customer import Customer


class Order(BaseModel):
    id_order: int
    customer: Customer
    address: Address
    bundles: list[AbstractBundle]
    status: str
