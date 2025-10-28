import pytest
from pydantic_core import ValidationError

from src.Model.discounted_bundle import DiscountedBundle
from src.Model.item import Item


def test_discounted_bundle_constructor_ok():
    item1 = Item(id_item=1, name="Galette", item_type="main", price=4.5)
    item2 = Item(id_item=2, name="Cidre", item_type="drink", price=3.0)
    bundle = DiscountedBundle(
        id_bundle=3,
        name="Breton Combo",
        components=["main", "drink"],
        discount=0.1,
        composition=[item1, item2],
    )

    assert bundle.id_bundle == 3
    assert bundle.name == "Breton Combo"
    assert bundle.discount == 0.1
    assert len(bundle.composition) == 2
    assert bundle.composition[1].name == "Cidre"


def test_discounted_bundle_invalid_discount_type():
    item = Item(id_item=1, name="Galette", item_type="main", price=4.5)
    with pytest.raises(ValidationError):
        DiscountedBundle(
            id_bundle=3,
            name="Breton Combo",
            components=["main", "drink"],
            discount="10 percent",
            composition=[item],
        )
