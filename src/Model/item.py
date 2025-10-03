from pydantic import BaseModel


class Item(BaseModel):
    id: int
    name: str
    description: str
    price: float
    item_type: str
    stock: int
    availability: bool
