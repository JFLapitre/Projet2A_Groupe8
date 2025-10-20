from datetime import date
from typing import Optional

from pydantic import ConfigDict

from src.Model.abstract_user import AbstractUser


class Customer(AbstractUser):
    id_user: int
    username: str
    password: str
    sign_up_date: date  # Accepte un objet date
    phone_number: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
