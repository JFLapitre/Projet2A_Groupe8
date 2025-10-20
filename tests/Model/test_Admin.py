import pytest
from pydantic_core import ValidationError

from src.Model.admin import Admin
from src.Model.item import Item
from src.Model.order import Order


def test_admin_constructor_ok():
    item = Item(id_item=1, name="Burger", item_type="main", price=5.0)
    order = Order(
        id=1,
        customer=42,
        adress="EJR HQ",
        bundles=[],
        items=[item],
        status="pending",
    )
    admin = Admin(
        id_user=1,
        username="admin",
        password="secure",
        sign_up_date=None,
        adress="EJR HQ",
        queue=[order],
    )

    assert admin.id_user == 1
    assert admin.username == "admin"
    assert admin.adress == "EJR HQ"
    assert isinstance(admin.queue, list)
    assert admin.queue[0].status == "pending"
    assert admin.queue[0].items[0].name == "Burger"


def test_admin_invalid_id_raises_validationerror():
    item = Item(id_item=1, name="Burger", item_type="main", price=5.0)
    order = Order(
        id=1,
        customer=42,
        adress="EJR HQ",
        bundles=[],
        items=[item],
        status="pending",
    )

    with pytest.raises(ValidationError):
        Admin(
            id_user="one",
            username="admin",
            password="secure",
            sign_up_date=None,
            adress="EJR HQ",
            queue=[order],
        )
