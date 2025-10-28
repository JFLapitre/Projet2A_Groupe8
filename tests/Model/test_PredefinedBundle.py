import pytest
from pydantic_core import ValidationError

from src.Model.item import Item
from src.Model.predefined_bundle import PredefinedBundle


def test_predefined_bundle_constructor_ok():
    item = Item(id_item=1, name="Galette", item_type="main", price=4.5)
    bundle = PredefinedBundle(id_bundle=1, name="Classic", composition=[item], price=4.5)

    assert bundle.id_bundle == 1
    assert bundle.name == "Classic"
    assert bundle.price == 4.5
    assert isinstance(bundle.composition, list)
    assert bundle.composition[0].name == "Galette"


def test_predefined_bundle_invalid_price_type():
    item = Item(id_item=1, name="Galette", item_type="main", price=4.5)
    with pytest.raises(ValidationError):
        PredefinedBundle(id_bundle=1, name="Classic", composition=[item], price="four")

