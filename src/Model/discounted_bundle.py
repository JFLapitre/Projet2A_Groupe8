from abstract_bundle.py import AbstractBundle
from item.py import Item


class DiscountedBundle(AbstractBundle):
    components: list[str]
    discount: float
    composition: list[Item]
