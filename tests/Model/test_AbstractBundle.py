import pytest
from pydantic_core import ValidationError

from src.Model.abstract_bundle import AbstractBundle


# Sous-classe concrète temporaire pour les tests
class DummyBundle(AbstractBundle):
    price: float = 0.0


def test_dummy_bundle_inherits_abstract_bundle_fields():
    bundle = DummyBundle(id_bundle=1, name="Test Bundle", price=9.99)
    assert bundle.id_bundle == 1
    assert bundle.name == "Test Bundle"
    assert bundle.price == 9.99


def test_dummy_bundle_invalid_id_raises():
    with pytest.raises(ValidationError):
        DummyBundle(id_bundle="abc", name="Invalid", price=3.0)
