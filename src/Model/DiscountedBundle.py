from AbstractBundle.py import AbstractBundle
from Item.py import Item


class DiscountedBundle(AbstractBundle):
    components: list[str]
    discount: float
    composition: list[Item]

