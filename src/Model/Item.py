from pydantic import BaseModel


class Item(BaseModel):
    id: int
    name: str
    description: str
    price: float
    itemtype: str
    stock: int
    availability: bool

