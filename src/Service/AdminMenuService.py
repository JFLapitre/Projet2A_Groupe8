from src.DAO.BundleDAO import BundleDAO
from src.DAO.ItemDAO import ItemDAO
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
        self.item_dao.add(new_item)  # méthode de la DAO

    def update_item(self, id: str, desc: str, price: float, stock: int, availability: bool) -> None:
        item = ItemDAO.get_by_id(id)  # type Item

        item.description = desc

        # always have a positive price
        if price > 0:
            item.price = price

        item.stock = stock
        item.availability = availability

        ItemDAO.update(item)

    def delete_item(self, id: str) -> None:
        pass

    def create_predefined(self, name: str, composition: list, price: float) -> PredefinedBundle:
        pass

    def create_discounted_bundle(self, name: str, components: list, discount: float) -> DiscountedBundle:
        pass

    def delete_bundle(self, id: str) -> None:
        pass

    def list_items(self) -> list[Item]:
        pass

    def list_bundles(self) -> list[Bundle]:
        pass
