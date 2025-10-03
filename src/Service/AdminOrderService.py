from typing import List

from src.DAO.DeliveryDAO import DeliveryDAO
from src.DAO.OrderDAO import OrderDAO
from src.Model.Delivery import Delivery
from src.Model.Order import Order


class AdminOrderService:
    def __init__(self):
        self.order_dao = OrderDAO()
        self.delivery_dao = DeliveryDAO()

    def list_waiting_orders(self) -> List[Order]:
        pass

    def list_deliveries(self) -> List[Delivery]:
        pass
