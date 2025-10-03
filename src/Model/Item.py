from pydantic import BaseModel


class Item(BaseModel):
    id: int
    name: str
    description: str
    price: float
    itemtype: str
    stock: int
    availability: bool

item = Item(id = 1, name = 'b', description = 'b', price = 3.2, itemtype = 'dessert', stock = 3, availability = True)
print(item)