from datetime import datetime
from typing import List, Optional

from src.DAO.addressDAO import AddressDAO
from src.DAO.bundleDAO import BundleDAO
from src.DAO.DBConnector import DBConnector
from src.DAO.itemDAO import ItemDAO
from src.DAO.orderDAO import OrderDAO
from src.DAO.userDAO import UserDAO
from src.Model.customer import Customer
from src.Model.order import Order


class OrderService:
    def __init__(self, db_connector: DBConnector):
        """
        Initializes the service and injects dependencies into the DAOs.
        """
        # DAOs must be initialized in order of dependency
        self.item_dao = ItemDAO(db_connector=db_connector)
        self.user_dao = UserDAO(db_connector=db_connector)
        self.address_dao = AddressDAO(db_connector=db_connector)
        self.bundle_dao = BundleDAO(db_connector=db_connector, item_dao=self.item_dao)

        # OrderDAO needs the other DAOs
        self.order_dao = OrderDAO(
            db_connector=db_connector,
            user_dao=self.user_dao,
            address_dao=self.address_dao,
            bundle_dao=self.bundle_dao,
        )

    def create_order(self, customer_id: int, address_id: int) -> Optional[Order]:
        """
        Creates a new, empty order for a specific customer and address.
        The order is created with a 'pending' status.
        """
        customer = self.user_dao.find_user_by_id(customer_id)
        if not customer or not isinstance(customer, Customer):
            raise ValueError(f"No valid customer found with ID {customer_id}")

        address = self.address_dao.find_address_by_id(address_id)
        if not address:
            raise ValueError(f"No address found with ID {address_id}")

        new_order = Order(
            customer=customer,
            address=address,
            bundles=[],
            status="pending",
            order_date=datetime.now(),
        )

        created_order = self.order_dao.add_order(new_order)
        if not created_order:
            raise Exception("Failed to create the order in the database.")

        return created_order

    def cancel_order(self, order_id: int) -> bool:
        """
        Cancels an order by deleting it.
        Checks if the order exists before deletion.
        """
        order = self.order_dao.find_order_by_id(order_id)
        if not order:
            raise ValueError(f"No order found with ID {order_id}.")

        # We assume 'cancel' means 'delete' if the order hasn't been processed.
        # If 'cancel' means setting a status, you would use update_order instead.
        return self.order_dao.delete_order(order_id)

    def add_bundle_to_order(self, order_id: int, bundle_id: int) -> Optional[Order]:
        """
        Adds a bundle to an existing 'pending' order.
        Checks if the bundle is available (all items in it are available).
        """
        order = self.order_dao.find_order_by_id(order_id)
        if not order:
            raise ValueError(f"No order found with ID {order_id}.")

        if order.status != "pending":
            raise ValueError(f"Cannot modify an order with status '{order.status}'.")

        bundle = self.bundle_dao.find_bundle_by_id(bundle_id)
        if not bundle:
            raise ValueError(f"No bundle found with ID {bundle_id}.")

        not_available = []
        for item in bundle.composition:
            if not item.availability:
                not_available.append(item.name)

        if not_available:
            raise ValueError(
                f"Bundle '{bundle.name}' is unavailable because items in the list '{not_available}' are not available."
            )

        order.bundles.append(bundle)

        if not self.order_dao.update_order(order):
            raise Exception("Failed to update the order.")

        return self.order_dao.find_order_by_id(order_id)

    def validate_order(self, order_id: int) -> Optional[Order]:
        order = self.order_dao.find_order_by_id(order_id)
        if not order:
            raise ValueError(f"No order found with ID {order_id}.")

        if order.status != "pending":
            raise ValueError(f"Only 'pending' orders can be validated. Current status: '{order.status}'.")

        if not order.bundles:
            raise ValueError("Cannot validate an empty order.")

        items_needed = {}
        for bundle in order.bundles:
            for item in bundle.composition:
                item_id = item.id_item
                items_needed[item_id] = items_needed.get(item_id, 0) + 1

        items_to_update = []
        for item_id, quantity_needed in items_needed.items():
            fresh_item = self.item_dao.find_item_by_id(item_id)

            if not fresh_item:
                raise Exception(f"Item ID {item_id} required for order no longer exists.")

            if fresh_item.stock < quantity_needed:
                raise ValueError(
                    f"Not enough stock for item '{fresh_item.name}'. Needed: {quantity_needed}, Available: {fresh_item.stock}."
                )

            fresh_item.stock -= quantity_needed
            if fresh_item.stock == 0:
                fresh_item.availability = False

            items_to_update.append(fresh_item)

        for item_to_update in items_to_update:
            updated_item = self.item_dao.update_item(item_to_update)

            if not updated_item:
                raise Exception(f"Failed to update stock for item {item_to_update.id_item}. Validation aborted.")
        order.status = "validated"

        if not self.order_dao.update_order(order):
            raise Exception("Stock was updated, but failed to validate the order status.")

        return order

    def get_order_details(self, order_id: int) -> Optional[Order]:
        """
        Retrieves all details for a single order.
        """
        order = self.order_dao.find_order_by_id(order_id)
        if not order:
            raise ValueError(f"No order found with ID {order_id}.")
        return order

    def list_orders_for_customer(self, customer_id: int) -> List[Order]:
        """
        Retrieves the order history for a specific customer.
        """
        customer = self.user_dao.find_user_by_id(customer_id)
        if not customer or not isinstance(customer, Customer):
            raise ValueError(f"No valid customer found with ID {customer_id}")

        return self.order_dao.find_orders_by_customer(customer_id)
