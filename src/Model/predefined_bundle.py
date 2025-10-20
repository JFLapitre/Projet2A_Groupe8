from src.Model.abstract_bundle import AbstractBundle
from src.Model.item import Item


class PredefinedBundle(AbstractBundle):
    composition: list[Item]
    price: float
