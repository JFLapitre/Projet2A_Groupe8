from abstract_bundle.py import AbstractBundle
from item.py import Item


class PredefinedBundle(AbstractBundle):
    composition: list[Item]
    price: float
