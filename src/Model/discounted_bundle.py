from typing import Optional

from src.Model.abstract_bundle import AbstractBundle
from src.Model.item import Item


class DiscountedBundle(AbstractBundle):
    required_item_types: list[str]
    discount: float
    composition: list[Item]
