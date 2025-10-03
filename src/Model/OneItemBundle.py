from AbstractBundle.py import AbstractBundle
from Item.py import Item


class OneItemBundle(AbstractBundle):
    composition: Item
    quantity: int
