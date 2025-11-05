# src/Model/one_item_bundle.py
from typing import List

from pydantic import Field

from src.Model.abstract_bundle import AbstractBundle
from src.Model.item import Item


class OneItemBundle(AbstractBundle):
    composition: List[Item] = Field(default_factory=list)

    def compute_price(self) -> float:
        """Price is the single item price."""
        if not self.composition:
            return 0.0
        return sum(item.price for item in self.composition)
