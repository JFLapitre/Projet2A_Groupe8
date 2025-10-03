from src.DAO.CustomerDAO import CustomerDAO
from src.Model.Customer import Customer
from src.Model.customer import Order


class OrderService:
    def __init__(self):
        self.customer_dao = CustomerDAO()
        self.order = Order()

    def create_order(self, Customer) -> Order:
        pass

    def cancel_order(self):
        pass

    def add_bundle_to_order(self):
        pass

    def create_doscounted_bundle(self):
        pass

    def validate_order(self):
        pass
