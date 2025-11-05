from typing import Optional

from pydantic import BaseModel


class Address(BaseModel):
    id_adress : Optional[int] = None
    city: str
    postal_code: int
    street_name: str
    street_number: Optional[int] = None
    extra_info: Optional[str] = None
