from typing import Optional

from pydantic import BaseModel


class Address(BaseModel):
    id_address : Optional[int] = None
    city: str
    postal_code: int
    street_name: str
    street_number: Optional[int] = None
