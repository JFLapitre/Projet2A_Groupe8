from types import Optional

from pydantic import BaseModel


class Address(BaseModel):
    city: str
    postal_code: str
    street_name: str
    street_number: Optional[int] = None
    extra_info: Optional[str] = None
