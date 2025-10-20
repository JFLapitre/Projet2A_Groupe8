from typing import Optional

from pydantic import BaseModel


class Item(BaseModel):
    id_item: Optional[int] = None
    name: str
    item_type: str
    price: float
