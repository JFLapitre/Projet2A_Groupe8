from typing import Optional

from src.Model.abstract_user import AbstractUser


class Driver(AbstractUser):
    id_user: Optional[int] = None
    name: str
    phone_number: str
    vehicle_type: str
    availability: bool
