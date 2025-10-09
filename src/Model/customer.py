from src.Model.abstract_user import AbstractUser
from pydantic import BaseModel, validator
from datetime import date
from typing import Optional

class Customer(AbstractUser):
    id_user: int
    username: str
    password: str
    sign_up_date: date  # Accepte un objet date
    phone_number: Optional[str] = None

    class Config:
        from_attributes = True  # Pour Pydantic v2
