from src.Model.abstract_user import AbstractUser


class Driver(AbstractUser):
    name: str = ""
    phone_number: str = ""
    vehicle_type: str
    availability: bool
