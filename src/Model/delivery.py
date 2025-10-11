from pydantic import BaseModel

from src.Model.driver import Driver
from src.Model.order import Order


class Delivery(BaseModel):
    id: int
    driver: Driver
    orders: list[Order]
    status: str
