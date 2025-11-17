import pytest
from pydantic_core import ValidationError

from src.Model.discounted_bundle import DiscountedBundle
from src.Model.item import Item


def test_discounted_bundle_ok():
    it1 = Item(name="A", item_type="x", price=2.0)
    it2 = Item(name="B", item_type="y", price=3.0)

    bundle = DiscountedBundle(
        id_bundle=1,
        name="Promo",
        required_item_types=["x", "y"],
        discount=0.2,
        composition=[it1, it2],
    )

    assert bundle.discount == 0.2
    assert len(bundle.composition) == 2


def test_invalid_discount_type():
    it = Item(name="A", item_type="x", price=2.0)

    with pytest.raises(ValidationError):
        DiscountedBundle(
            id_bundle=1,
            name="Promo",
            required_item_types=["x"],
            discount="twenty",
            composition=[it],
        )
