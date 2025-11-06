from src.DAO.addressDAO import AddressDAO
from src.DAO.bundleDAO import BundleDAO
from src.DAO.DBConnector import DBConnector
from src.DAO.itemDAO import ItemDAO
from src.DAO.orderDAO import OrderDAO
from src.DAO.userDAO import UserDAO
from src.Model.delivery import Delivery
from src.Model.order import Order


class AdminOrderService:
    def __init__(self, db_connector: DBConnector):
        self.item_dao = ItemDAO(db_connector=db_connector)
        self.user_dao = UserDAO(db_connector=db_connector)
        self.address_dao = AddressDAO(db_connector=db_connector)

        self.bundle_dao = BundleDAO(db_connector=db_connector, item_dao=self.item_dao)

        self.order_dao = OrderDAO(
            db_connector=db_connector,
            item_dao=self.item_dao,
            user_dao=self.user_dao,
            address_dao=self.address_dao,
            bundle_dao=self.bundle_dao,
        )

    def list_waiting_orders(self) -> list[Order]:
        all_orders = self.order_dao.find_all_orders()
        return [order for order in all_orders if order.status == "pending"]

    def list_deliveries(self) -> list[Delivery]:
        return self.delivery_dao.list_deliveries()
