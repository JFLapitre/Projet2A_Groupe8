from src.DAO.CustomerDAO import CustomerDAO
from src.Model.Customer import Customer


# à modifer
def hash_function(string: str) -> str:
    pass


class AuthenticationService:
    def __init__(self):
        self.customer_dao = CustomerDAO()

    def login(self, id: str, password: str) -> Customer:
        customer = self.customer_dao.find_by_id(id)
        if not customer:
            raise ValueError("User not found")

        hash_in_db = self.customer_dao.find_hashed_password_by_id(id)  # à implémenter

        if hash_function(password) != hash_in_db:
            raise ValueError("Incorrect password")

        return customer

    def register(self, id: str, name: str, password: str, default_address: str) -> Customer:
        if self.customer_dao.find_by_id(id):
            raise ValueError(f"User with id {id} already exists")

        if not id or not name or not password:
            raise ValueError("id, name, and password are required")

        hashed_password = hash_function(password)

        new_customer = Customer(id=id, name=name, password=hashed_password, default_address=default_address)

        self.customer_dao.add_customer(new_customer)  # à implémenter
        return new_customer
