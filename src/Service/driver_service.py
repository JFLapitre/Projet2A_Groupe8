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


class DriverService:
    def __init__(self, db_connector: DBConnector):
        """
        Initializes the service and injects dependencies into the DAOs.
        (This part is unchanged, it is well-structured)
        """
        self.db_connector = db_connector  # Store the connector for transactions
        self.item_dao = ItemDAO(db_connector=db_connector)
        self.user_dao = UserDAO(db_connector=db_connector)
        self.address_dao = AddressDAO(db_connector=db_connector)
        self.bundle_dao = BundleDAO(db_connector=db_connector, item_dao=self.item_dao)

        self.order_dao = OrderDAO(
            db_connector=db_connector,
            user_dao=self.user_dao,
            address_dao=self.address_dao,
            bundle_dao=self.bundle_dao,
        )

        self.delivery_dao = DeliveryDAO(db_connector=db_connector, user_dao=self.user_dao, order_dao=self.order_dao)

    def create_and_assign_delivery(self, order_ids: List[int], driver_id: int) -> Optional[Delivery]:
        """
        Creates a new delivery run from a list of 'pending' order IDs and
        immediately assigns it to the specified available driver.
        """
        if not order_ids:
            raise ValueError("Cannot create a delivery with no orders.")

        driver = self.user_dao.find_user_by_id(driver_id)
        if not driver or not isinstance(driver, Driver):
            raise ValueError(f"No valid driver found with ID {driver_id}")

        if not driver.availability:
            raise ValueError(f"Driver {driver.name} is not available to start a new delivery.")

        orders = []
        for order_id in order_ids:
            order = self.order_dao.find_order_by_id(order_id)
            if not order:
                raise ValueError(f"Order {order_id} not found.")
            if order.status != "pending":
                raise ValueError(f"Order {order_id} is not in 'pending' status. Current status: {order.status}")
            orders.append(order)

        for o in orders:
            o.status = "in_progress"
            self.order_dao.update_order(o)

        new_delivery = Delivery(
            driver=driver,
            orders=orders,
            status="in_progress",
            delivery_time=None,
        )
        try:
            created_delivery = self.delivery_dao.add_delivery(new_delivery)
            if not created_delivery:
                raise Exception("Failed to create the delivery in the database.")

            for o in created_delivery.orders:
                o.status = "in_progress"
                if not self.order_dao.update_order(o):
                    raise Exception(f"Failed to update status for order {o.id_order}")

            self.db_connector()
            logging.info(f"Delivery {created_delivery.id_delivery} created and assigned to driver {driver_id}.")
            return created_delivery

        except Exception as e:
            logging.error(f"Failed to create delivery for driver {driver_id}: {e}")
            self.db_connector.rollback()
            raise e

    def complete_delivery(self, delivery_id: int) -> Optional[Delivery]:
        """
        Marks a delivery as 'completed' and updates the status
        of all associated orders to 'delivered'.

        This operation is transactional.
        """
        delivery = self.delivery_dao.find_delivery_by_id(delivery_id)
        if not delivery:
            raise ValueError(f"No delivery found with ID {delivery_id}.")

        if delivery.status != "in_progress":
            raise ValueError(f"Only 'in_progress' deliveries can be completed. Current status: {delivery.status}")

        try:
            delivery.status = "completed"
            delivery.delivery_time = datetime.now()

            if not self.delivery_dao.update_delivery(delivery):
                raise Exception("Failed to update the delivery status.")
            for order in delivery.orders:
                order.status = "delivered"
                if not self.order_dao.update_order(order):
                    # If one order fails, the whole transaction is rolled back
                    raise Exception(f"Failed to update status for order {order.id_order}")
            self.db_connector.commit()
            logging.info(f"Delivery {delivery_id} completed successfully.")
            return delivery

        except Exception as e:
            logging.error(f"Failed to complete delivery {delivery_id}: {e}")
            self.db_connector.rollback()
            raise e

    def get_delivery_details(self, delivery_id: int) -> Optional[Delivery]:
        """
        Retrieves all details for a single delivery.
        (Logic unchanged, it is simple and correct)
        """
        delivery = self.delivery_dao.find_delivery_by_id(delivery_id)
        if not delivery:
            raise ValueError(f"No delivery found with ID {delivery_id}.")
        return delivery

    def list_pending_deliveries(self) -> List[Delivery]:
        """
        Returns a list of all deliveries with 'pending' status.
        """
        all_deliveries = self.delivery_dao.find_all_deliveries()
        return [d for d in all_deliveries if d.status == "pending"]
