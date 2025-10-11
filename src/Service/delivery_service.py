from src.DAO.DeliveryDAO import DeliveryDAO


class DeliveryService:
    def __init__(self):
        self.delivery_dao = DeliveryDAO()

    def start_delivery(self):
        pass

    def validate_delivery(self):
        self.delivery_dao.validate_delivery()
