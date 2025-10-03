import pytest
from src.services.admin_menu_service import AdminMenuService


@pytest.fixture
def admin_menu_service():
    return AdminMenuService()


@pytest.mark.parametrize(
    "name, desc, price, stock, availability, should_raise_error",
    [
        # Valid cases
        ("Valid Item", "Description", 10.99, 100, True, False),
        ("Valid Item", "Description", 10.99, 0, False, False),
        # Invalid cases
        ("Invalid Item", "Description", 10.99, 0, True, True),  # Stock is null but product is available
        ("", "Description", 10.99, 100, True, True),  # No name
        ("Invalid Item", "Description", -10.99, 100, True, True),  # Negative price
    ],
)
def test_create_item_with_various_inputs(
    admin_menu_service, name, desc, price, stock, availability, should_raise_error
):
    if should_raise_error:
        with pytest.raises(ValueError):
            admin_menu_service.create_item(name, desc, price, stock, availability)
    else:
        # Verify that the item was created succesfully
        result = admin_menu_service.create_item(name, desc, price, stock, availability)
        assert result.name == name
        assert result.stock == stock
        assert result.availability == availability
