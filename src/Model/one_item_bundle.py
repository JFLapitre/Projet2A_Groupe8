from src.Model.abstract_bundle import AbstractBundle
from src.Model.item import Item


class OneItemBundle(AbstractBundle):
    composition: Item

    def compute_price(self) -> float:
        """Price is the single item price."""
        return self.composition.price
