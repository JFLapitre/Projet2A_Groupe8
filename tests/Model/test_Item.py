import pytest
from pydantic_core import ValidationError

from src.Model.item import Item


def test_item_constructor_ok():
    banana = Item(name="banana", price=3.2, item_type="dessert")
    assert banana.name == "banana"
    assert banana.price == 3.2
    assert banana.item_type == "dessert"


def test_item_constructor_throws_on_incorrect_input():
    with pytest.raises(ValidationError) as exception_info:
        Item(name="banana", price="onéreux", item_type="dessert")
    assert "price" in str(exception_info.value)
