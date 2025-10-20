from abstract_bundle import AbstractBundle

from src.Model.item import Item


class DiscountedBundle(AbstractBundle):
    components: list[str]
    discount: float
    composition: list[Item]
