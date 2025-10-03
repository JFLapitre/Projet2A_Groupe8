from src.DAO.CustomerDAO import CustomerDAO
from src.Model.Customer import Customer


class AuthenticationService:
    def __init__(self):
        self.customer_dao = CustomerDAO()

    def login(self, id: str, password: str) -> None:
        pass

    def register(self, id: str, name: str, password: str, default_address: str) -> Customer:
        pass
