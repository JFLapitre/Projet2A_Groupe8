from src.Model.abstract_bundle import AbstractBundle
from src.Model.item import Item


class PredefinedBundle(AbstractBundle):
    composition: list[Item]
    price: float

    def compute_price(self) -> float:
        """Price is predefined for this bundle."""
        return self.price
