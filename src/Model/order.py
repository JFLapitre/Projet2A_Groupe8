from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from src.Model.address import Address
from src.Model.customer import Customer
from src.Model.item import Item


class Order(BaseModel):
    id_order: Optional[int] = None
    customer: Customer
    address: Address
    items: list[Item]
    price: Optional[float] = None
    status: str
    order_date: datetime = Field(default_factory=datetime.now)
