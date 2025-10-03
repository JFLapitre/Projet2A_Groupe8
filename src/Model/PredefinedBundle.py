from AbstractBundle.py import AbstractBundle
from Item.py import Item


class PredefinedBundle(AbstractBundle):
    composition: list[Item]
    price: float
