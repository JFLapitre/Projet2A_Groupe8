import logging
from datetime import datetime
from typing import List, Optional

from src.DAO.addressDAO import AddressDAO
from src.DAO.bundleDAO import BundleDAO
from src.DAO.DBConnector import DBConnector
from src.DAO.deliveryDAO import DeliveryDAO
from src.DAO.itemDAO import ItemDAO
from src.DAO.orderDAO import OrderDAO
from src.DAO.userDAO import UserDAO
from src.Model.delivery import Delivery
from src.Model.driver import Driver


class DeliveryService:
    def __init__(self, db_connector: DBConnector):
        """
        Initializes the service and injects dependencies into the DAOs.
        """
        # Initialisation dans l'ordre de dépendance
        self.item_dao = ItemDAO(db_connector=db_connector)
        self.user_dao = UserDAO(db_connector=db_connector)
        self.address_dao = AddressDAO(db_connector=db_connector)
        self.bundle_dao = BundleDAO(db_connector=db_connector, item_dao=self.item_dao)

        self.order_dao = OrderDAO(
            db_connector=db_connector,
            user_dao=self.user_dao,
            address_dao=self.address_dao,
            item_dao=self.item_dao,
            bundle_dao=self.bundle_dao,
        )

        self.delivery_dao = DeliveryDAO(db_connector=db_connector, user_dao=self.user_dao, order_dao=self.order_dao)

    def create_delivery(self, order_ids: List[int]) -> Optional[Delivery]:
        """
        Creates a new delivery run from a list of 'validated' order IDs.
        The delivery is created with a 'pending' status, awaiting a driver.
        """
        if not order_ids:
            raise ValueError("Cannot create a delivery with no orders.")

        orders = []
        for order_id in order_ids:
            order = self.order_dao.find_order_by_id(order_id)
            if not order:
                raise ValueError(f"Order with ID {order_id} not found.")
            if order.status != "validated":
                raise ValueError(f"Order {order_id} is not validated. Current status: {order.status}")
            orders.append(order)

        # The delivery is created without a driver and awaits assignment
        new_delivery = Delivery(driver=None, orders=orders, status="pending", delivery_time=None)

        created_delivery = self.delivery_dao.add_delivery(new_delivery)
        if not created_delivery:
            raise Exception("Failed to create the delivery in the database.")
        return created_delivery

    def assign_driver_to_delivery(self, delivery_id: int, driver_id: int) -> Optional[Delivery]:
        """
        Assigns an available driver to a pending delivery and sets its status to 'in_progress'.
        """
        delivery = self.delivery_dao.find_delivery_by_id(delivery_id)
        if not delivery:
            raise ValueError(f"No delivery found with ID {delivery_id}.")

        if delivery.status != "pending":
            raise ValueError(f"Delivery is not pending. Current status: {delivery.status}")

        driver = self.user_dao.find_user_by_id(driver_id)
        if not driver or not isinstance(driver, Driver):
            raise ValueError(f"No valid driver found with ID {driver_id}")

        if not driver.availability:
            raise ValueError(f"Driver {driver.name} is not available.")

        delivery.driver = driver
        delivery.status = "in_progress"

        if not self.delivery_dao.update_delivery(delivery):
            raise Exception("Failed to update delivery with new driver.")

        return delivery

    def complete_delivery(self, delivery_id: int) -> Optional[Delivery]:
        """
        Marks a delivery as 'completed' and sets the delivery time.
        This replaces the skeleton 'validate_delivery' method.
        """
        delivery = self.delivery_dao.find_delivery_by_id(delivery_id)
        if not delivery:
            raise ValueError(f"No delivery found with ID {delivery_id}.")

        if delivery.status != "in_progress":
            raise ValueError(f"Only 'in_progress' deliveries can be completed. Current status: {delivery.status}")

        delivery.status = "completed"
        delivery.delivery_time = datetime.now()

        try:
            for order in delivery.orders:
                order.status = "delivered"  # Assuming "delivered" is a valid status
                self.order_dao.update_order(order)
        except Exception as e:
            logging.warning(f"Could not update status for orders in delivery {delivery_id}: {e}")

        if not self.delivery_dao.update_delivery(delivery):
            raise Exception("Failed to update delivery status to completed.")

        return delivery

    def get_delivery_details(self, delivery_id: int) -> Optional[Delivery]:
        """
        Retrieves all details for a single delivery.
        """
        delivery = self.delivery_dao.find_delivery_by_id(delivery_id)
        if not delivery:
            raise ValueError(f"No delivery found with ID {delivery_id}.")
        return delivery

    def list_pending_deliveries(self) -> List[Delivery]:
        """
        Returns a list of all deliveries with 'pending' status (awaiting a driver).
        """
        all_deliveries = self.delivery_dao.find_all_deliveries()
        return [d for d in all_deliveries if d.status == "pending"]
