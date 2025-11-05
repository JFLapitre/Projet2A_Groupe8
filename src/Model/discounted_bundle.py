from typing import Optional

from src.Model.abstract_bundle import AbstractBundle
from src.Model.item import Item


class DiscountedBundle(AbstractBundle):
    required_item_types: list[str]
    discount: float
    composition: Optional[list[Item]] = []

    def compute_price(self) -> float:
        """Sum the price of all items and apply discount."""
        total = sum(item.price for item in self.composition)
        return total * (1 - self.discount)
