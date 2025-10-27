from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.Model.driver import Driver
from src.Model.order import Order


class Delivery(BaseModel):
    id_delivery: int
    driver: Optional[Driver]
    orders: list[Order]
    status: str
    delivery_time: Optional[datetime] = None
