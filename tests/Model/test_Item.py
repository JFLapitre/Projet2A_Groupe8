import pytest
from pydantic_core import ValidationError

from src.Model.item import Item


def test_item_constructor_ok():
    banana = Item(id = 12, name = 'banana', description = "It's yellow", price = 3.2, itemtype = 'dessert', stock = 3, availability = True)
    assert banana.id == 12
    assert banana.name == "banana"
    assert banana.description == "It's yellow"
    assert banana.price == 3.2
    assert banana.itemtype == "dessert"
    assert banana.stock == 3
    assert banana.availability



def test_item_constructor_throws_on_incorrect_input():
    with pytest.raises(ValidationError) as exception_info:
        Item(id="Twelve", name = 'banana', description = "It's yellow", price = 3.2, itemtype = 'dessert', stock = 3, availability = True)
    assert "id" in str(
        exception_info.value
    ) and "Input should be a valid integer, unable to parse string as an integer" in str(exception_info.value)
