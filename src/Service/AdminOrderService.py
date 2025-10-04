from src.DAO.DeliveryDAO import DeliveryDAO
from src.DAO.OrderDAO import OrderDAO
from src.Model.Delivery import Delivery
from src.Model.Order import Order


class AdminOrderService:
    def __init__(self):
        self.order_dao = OrderDAO()
        self.delivery_dao = DeliveryDAO()

    def list_waiting_orders(self) -> list[Order]:
        all_orders = self.order_dao.list_all_orders()  # à implémenter
        return [order for order in all_orders if order.status == "Waiting"]

    def list_deliveries(self) -> list[Delivery]:
        return self.delivery_dao.list_deliveries()  # à implémenter
