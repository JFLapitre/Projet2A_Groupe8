import pytest
from pydantic_core import ValidationError

from src.Model.item import Item
from src.Model.one_item_bundle import OneItemBundle


def test_one_item_bundle_constructor_ok():
    item = Item(id_item=1, name="Coca-Cola", item_type="drink", price=2.0)
    bundle = OneItemBundle(id_bundle=2, name="Single Drink", composition=item)

    assert bundle.id_bundle == 2
    assert bundle.name == "Single Drink"
    assert bundle.composition.name == "Coca-Cola"
    assert bundle.composition.price == 2.0


def test_one_item_bundle_invalid_composition_type():
    with pytest.raises(ValidationError):
        OneItemBundle(id_bundle=2, name="Invalid", composition="not_an_item")
