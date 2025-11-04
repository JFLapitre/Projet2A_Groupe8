from datetime import date
from typing import Optional

from pydantic import ConfigDict, Field

from src.Model.abstract_user import AbstractUser


class Customer(AbstractUser):
    name: str = ""
    sign_up_date: date = Field(default_factory=date.today)
    phone_number: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
