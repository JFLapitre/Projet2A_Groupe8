from pydantic import BaseModel


class Address(BaseModel):
    city: str
    postal_code: str
    street_name: str
    street_number: int
