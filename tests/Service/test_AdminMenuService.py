import pytest

from src.services.admin_menu_service import AdminMenuService


@pytest.fixture
def admin_menu_service():
    return AdminMenuService()

# Test create_item
@pytest.mark.parametrize(
    "name, desc, price, stock, availability, should_raise_error, error_message",
    [
        # Valid cases
        ("Valid Item", "Description", 10.99, 100, True, False, None),
        ("Valid Item", "Description", 10.99, 0, False, False, None),
        # Invalid cases
        ("Invalid Item", "Description", 10.99, 0, True, True, "Zero stock implies non-availability"),
        ("", "Description", 10.99, 100, True, True, "A name should be entered"),
        ("Invalid Item", "Description", -10.99, 100, True, True, "Price must be positice"),
    ],
)
def test_create_item_with_various_inputs(
    admin_menu_service, name, desc, price, stock, availability, should_raise_error, error_message
):
    if should_raise_error:
        with pytest.raises(ValueError) as excinfo:
            admin_menu_service.create_item(name, desc, price, stock, availability)
        assert error_message in str(excinfo.value)
    else:
        # Verify that the item was created succesfully
        result = admin_menu_service.create_item(name, desc, price, stock, availability)
        assert result.name == name
        assert result.stock == stock
        assert result.availability == availability

# Test update_item
@pytest.fixture
def admin_menu_service():
    return AdminMenuService()

@pytest.mark.parametrize(
    "id, desc, price, stock, availability, should_raise_error, error_message",
    [
        # Valid cases
        ("Id", "New Description", 12.99, 200, True, False, None),
        ("Id", "New Description", 12.99, 0, False, False, None),

        # Invalid cases
        ("Id", "New Description", -12.99, 200, True, True, "Price must be positive"),
        ("Wrong Id", "New Description", 12.99, 200, True, True, "No item found"),
        ("Id", "New Description", 12.99, -2, False, True, "Stock cannot be negative"),
        ("Id", "New Description", 12.99, 0, True, True, "Zero stock implies non-availability"),
    ],
)
def test_update_item_with_various_inputs(
    admin_menu_service, id, desc, price, stock, availability, should_raise_error, error_message
):
    if id == 1 and not should_raise_error:
        admin_menu_service.create_item("Id", "Initial Description", 10.99, 100, True)

    if should_raise_error:
        with pytest.raises(ValueError) as excinfo:
            admin_menu_service.update_item(id, desc, price, stock, availability)
        assert error_message in str(excinfo.value)
    else:
        result = admin_menu_service.update_item(id, desc, price, stock, availability)
        assert result.description == desc
        assert result.price == price
        assert result.stock == stock
        assert result.availability == availability

# Test delete_item
@pytest.mark.parametrize(
    "id, should_raise_error, error_message",
    [
        # Valid cases
        ("Id", False, None),

        # Invalid cases
        ("Wrong Id", True, "No item found"),
    ],
)
def test_delete_item_with_various_inputs(
    admin_menu_service, id, should_raise_error, error_message
):
    if id == "Id" and not should_raise_error:
        admin_menu_service.create_item(id, "Description", 12.99, 200, True)

    if should_raise_error:
        with pytest.raises(ValueError) as excinfo:
            admin_menu_service.delete_item(id)
        assert error_message in str(excinfo.value)
    else:
        admin_menu_service.delete_item(id)
