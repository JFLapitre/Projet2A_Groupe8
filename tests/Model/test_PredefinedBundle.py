from src.Model.item import Item
from src.Model.predefined_bundle import PredefinedBundle


def test_predefined_bundle_constructor():
    item = Item(name="Galette", item_type="main", price=4.5)
    bundle = PredefinedBundle(id=1, name="Classic", composition=[item], price=4.5)

    assert bundle.name == "Classic"
    assert bundle.price == 4.5
    assert bundle.composition[0].name == "Galette"
