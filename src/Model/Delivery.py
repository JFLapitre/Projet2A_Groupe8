from DriverUser.py import DriverUser
from Order.py import Order
from pydantic import BaseModel


class Delivery(BaseModel):
    id : int
    driver : DriverUser
    orders : list[Order]
    status : str
