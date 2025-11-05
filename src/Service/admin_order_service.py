from src.DAO.deliveryDAO import DeliveryDAO
from src.DAO.orderDAO import OrderDAO
from src.Model.delivery import Delivery
from src.Model.order import Order


class AdminOrderService:
    def __init__(self, delivery_dao: DeliveryDAO, order_dao: OrderDAO ):
        self.order_dao = order_dao
        self.delivery_dao = delivery_dao

    def list_waiting_orders(self) -> list[Order]:
        all_orders = self.order_dao.find_all_orders()
        return [order for order in all_orders if order.status == "pending"]

    def list_deliveries(self) -> list[Delivery]:
        return self.delivery_dao.list_deliveries()
