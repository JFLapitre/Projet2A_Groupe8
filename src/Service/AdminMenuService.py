from src.DAO.BundleDAO import BundleDAO
from src.DAO.itemDAO import ItemDAO
from src.Model.Bundle import Bundle
from src.Model.DiscountedBundle import DiscountedBundle
from src.Model.Item import Item
from src.Model.PredeinedBundle import PredefinedBundle


class AdminMenuService:
    def __init__(self):
        self.item_dao = ItemDAO()
        self.bundle_dao = BundleDAO()

    def create_item(self, name: str, desc: str, price: float, stock: int, availability: bool) -> None:
        """Create a new item"""
        if price < 0:
            raise ValueError("Price must be positive.")
        if stock < 0:
            raise ValueError("Stock cannot be negative.")
        if stock == 0:
            assert not availability, "Zero stock implies non-availability"

        new_item = Item(name=name, description=desc, price=price, stock=stock, availability=availability)
        self.item_dao.add_item(new_item)

    def update_item(self, id: str, desc: str, price: float, stock: int, availability: bool) -> None:
        item = self.item_dao.find_item_by_id(id)
        if not item:
            raise ValueError(f"No item found with id {id}.")
        if price >= 0:
            item.price = price
        else:
            raise ValueError("Price must be positive.")
        if stock < 0:
            raise ValueError("Stock cannot be negative.")
        if stock == 0:
            assert not availability, "Zero stock implies non-availability"

        item.description = desc
        item.stock = stock
        item.availability = availability
        self.item_dao.update_item(item)

    def delete_item(self, id: str) -> None:
        item = self.item_dao.find_item_by_id(id)
        if not item:
            raise ValueError(f"No item found with id {id}.")

        self.item_dao.delete_item(id)

    def create_predefined_bundle(self, name: str, composition: list, price: float) -> None:
        if price <= 0:
            raise ValueError("Price must be positive.")
        if not composition:
            raise ValueError("Composition cannot be empty.")

        new_bundle = PredefinedBundle(name=name, composition=composition, price=price)
        self.bundle_dao.add_predifined_bundle(new_bundle)  # à implémenter

    def create_discounted_bundle(self, name: str, components: list, discount: float) -> None:
        if discount <= 0 or discount >= 100:
            raise ValueError("Discount must be between 0 and 100.")
        if not components:
            raise ValueError("Components list cannot be empty.")

        new_bundle = DiscountedBundle(name=name, components=components, discount=discount)
        self.bundle_dao.add_dicounted_bundle(new_bundle)  # à implémenter

    def delete_bundle(self, id: str) -> None:
        if not self.bundle_dao.find_bundle_by_id(id):  # à implémenter
            raise ValueError(f"No bundle found with id {id}.")
        self.bundle_dao.delete_bundle(id)  # à implémenter

    def list_items(self) -> list[Item]:
        self.item_dao.find_all_items()

    def list_bundles(self) -> list[Bundle]:
        self.bundle_dao.find_all_bundles()
