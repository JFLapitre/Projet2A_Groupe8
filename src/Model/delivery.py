from driver.py import Driver
from order.py import Order
from pydantic import BaseModel


class Delivery(BaseModel):
    id : int
    driver : Driver
    orders : list[Order]
    status : str
