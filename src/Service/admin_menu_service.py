from src.DAO.bundleDAO import BundleDAO
from src.DAO.DBConnector import DBConnector
from src.DAO.itemDAO import ItemDAO
from src.Model.abstract_bundle import AbstractBundle
from src.Model.discounted_bundle import DiscountedBundle
from src.Model.item import Item
from src.Model.one_item_bundle import OneItemBundle
from src.Model.predefined_bundle import PredefinedBundle


class AdminMenuService:
    def __init__(self, db_connector: DBConnector):
        """
        Initializes the service and injects dependencies into the DAOs.
        """
        self.item_dao = ItemDAO(db_connector=db_connector)
        self.bundle_dao = BundleDAO(db_connector=db_connector, item_dao=self.item_dao)

    def create_item(self, name: str, desc: str, price: float, stock: int, availability: bool, item_type: str) -> None:
        """
        Validates and creates a new item in the database.
        """
        if price < 0:
            raise ValueError("Price must be positive.")
        if stock < 0:
            raise ValueError("Stock cannot be negative.")
        if stock == 0 and availability:
            raise ValueError("Zero stock implies non-availability.")

        new_item = Item(
            name=name, description=desc, price=price, stock=stock, availability=availability, item_type=item_type
        )
        created_item = self.item_dao.add_item(new_item)
        if not created_item:
            raise Exception(f"Failed to create item: {name}")

    def update_item(
        self, id: int, name: str, desc: str, price: float, stock: int, availability: bool, item_type: str
    ) -> None:
        """
        Finds an existing item by ID, validates new data, and updates it.
        """
        item = self.item_dao.find_item_by_id(id)
        if not item:
            raise ValueError(f"No item found with ID {id}.")

        if price >= 0:
            item.price = price
        else:
            raise ValueError("Price must be positive.")

        if stock < 0:
            raise ValueError("Stock cannot be negative.")
        if stock == 0 and availability:
            raise ValueError("Zero stock implies non-availability.")

        # Update all fields
        item.name = name
        item.description = desc
        item.stock = stock
        item.availability = availability
        item.item_type = item_type

        updated_item = self.item_dao.update_item(item)
        if not updated_item:
            raise Exception(f"Failed to update item: {id}")

    def delete_item(self, id: int) -> None:
        """
        Finds an item by ID and deletes it from the database.
        """
        item = self.item_dao.find_item_by_id(id)
        if not item:
            raise ValueError(f"No item found with ID {id}.")

        if not self.item_dao.delete_item(id):
            raise Exception(f"Failed to delete item: {id}")

    def create_predefined_bundle(
        self, name: str, description: str, composition: list, availability: bool, price: float
    ) -> None:
        """
        Validates and creates a new predefined (fixed-price) bundle.
        """
        if price <= 0:
            raise ValueError("Price must be positive.")
        if not composition:
            raise ValueError("Composition cannot be empty.")

        new_bundle = PredefinedBundle(
            name=name, description=description, composition=composition, price=price, availability=availability
        )
        created_bundle = self.bundle_dao.add_predefined_bundle(new_bundle)
        if not created_bundle:
            raise Exception(f"Failed to create predefined bundle: {name}")

    """def create_one_item_bundle(self, name: str, description: str, price: float, item: Item) -> None:
        if price <= 0:
            raise ValueError("Price must be positive.")
        if not item:
            raise ValueError("Item cannot be null.")

        new_bundle = OneItemBundle(name=name, description=description, price=price, composition=item)
        created_bundle = self.bundle_dao.add_one_item_bundle(new_bundle)
        if not created_bundle:
            raise Exception(f"Failed to create one-item bundle: {name}")"""

    def create_discounted_bundle(self, name: str, description: str, required_item_types: list, discount: float) -> None:
        """
        Validates and creates a new bundle that applies a discount.
        """
        if not (0 < discount < 100):
            raise ValueError("Discount must be between 0 and 100 (exclusive).")
        if not required_item_types:
            raise ValueError("Item types cannot be empty.")

        new_bundle = DiscountedBundle(
            name=name, description=description, required_item_types=required_item_types, discount=discount
        )
        created_bundle = self.bundle_dao.add_discounted_bundle(new_bundle)
        if not created_bundle:
            raise Exception(f"Failed to create discounted bundle: {name}")

    def delete_bundle(self, id: int) -> None:
        """
        Finds a bundle by ID and deletes it from the database.
        """
        if not self.bundle_dao.find_bundle_by_id(id):
            raise ValueError(f"No bundle found with ID {id}.")

        if not self.bundle_dao.delete_bundle(id):
            raise Exception(f"Failed to delete bundle: {id}")

    def list_items(self) -> list[Item]:
        """
        Retrieves a list of all items from the database.
        """
        return self.item_dao.find_all_items()

    def list_bundles(self) -> list[AbstractBundle]:
        """
        Retrieves a list of all bundles from the database.
        """
        return self.bundle_dao.find_all_bundles()
