from unittest.mock import ANY, MagicMock

import pytest

from src.DAO.bundleDAO import BundleDAO
from src.DAO.DBConnector import DBConnector
from src.DAO.itemDAO import ItemDAO
from src.Model.abstract_bundle import AbstractBundle
from src.Model.discounted_bundle import DiscountedBundle
from src.Model.item import Item
from src.Model.predefined_bundle import PredefinedBundle
from src.Service.admin_menu_service import AdminMenuService


@pytest.fixture
def mock_db_connector():
    return MagicMock(spec=DBConnector)


@pytest.fixture
def mock_item_dao():
    return MagicMock(spec=ItemDAO)


@pytest.fixture
def mock_bundle_dao():
    return MagicMock(spec=BundleDAO)


@pytest.fixture
def service(mock_db_connector, mock_item_dao, mock_bundle_dao, mocker):
    mocker.patch("src.Service.admin_menu_service.ItemDAO", return_value=mock_item_dao)
    mocker.patch("src.Service.admin_menu_service.BundleDAO", return_value=mock_bundle_dao)
    admin_service = AdminMenuService(db_connector=mock_db_connector)
    return admin_service


@pytest.fixture
def sample_item():
    return Item(id=1, name="Test Item", description="Desc", price=10.0, stock=5, availability=True, item_type="TypeA")


@pytest.fixture
def sample_item_list(sample_item):
    item2 = Item(
        id=2, name="Test Item 2", description="Desc 2", price=20.0, stock=10, availability=True, item_type="TypeB"
    )
    return [sample_item, item2]


@pytest.fixture
def sample_item_types():
    return ["Boisson", "Plat", "Dessert"]


@pytest.fixture
def sample_bundle():
    return MagicMock(spec=AbstractBundle)


def test_create_item_success(service: AdminMenuService, mock_item_dao: MagicMock):
    """Tests successful creation of a valid item."""
    mock_item_dao.add_item.return_value = MagicMock(spec=Item)

    service.create_item("New Item", "Desc", 15.0, 10, True, "TypeB")

    mock_item_dao.add_item.assert_called_once_with(ANY)
    called_item = mock_item_dao.add_item.call_args[0][0]
    assert isinstance(called_item, Item)
    assert called_item.name == "New Item"
    assert called_item.price == 15.0


def test_create_item_validation_negative_price(service: AdminMenuService):
    """Tests that creating an item with a negative price raises a ValueError."""
    with pytest.raises(ValueError, match="Price must be positive."):
        service.create_item("Bad Item", "Desc", -10.0, 5, True, "TypeA")


def test_create_item_validation_negative_stock(service: AdminMenuService):
    """Tests that creating an item with negative stock raises a ValueError."""
    with pytest.raises(ValueError, match="Stock cannot be negative."):
        service.create_item("Bad Item", "Desc", 10.0, -5, True, "TypeA")


def test_create_item_validation_zero_stock_available(service: AdminMenuService):
    """Tests that zero stock and availability=True raises a ValueError."""
    with pytest.raises(ValueError, match="Zero stock implies non-availability."):
        service.create_item("Out of Stock", "Desc", 10.0, 0, True, "TypeA")


def test_create_item_dao_failure(service: AdminMenuService, mock_item_dao: MagicMock):
    """Tests that an Exception is raised if the DAO fails to create the item."""
    mock_item_dao.add_item.return_value = None

    with pytest.raises(Exception, match="Failed to create item: New Item"):
        service.create_item("New Item", "Desc", 15.0, 10, True, "TypeB")


def test_update_item_success(service: AdminMenuService, mock_item_dao: MagicMock, sample_item: Item):
    """Tests successful update of an existing item."""
    mock_item_dao.find_item_by_id.return_value = sample_item
    mock_item_dao.update_item.return_value = sample_item

    service.update_item(1, "Updated Name", "Updated Desc", 20.0, 15, True, "TypeC")

    mock_item_dao.find_item_by_id.assert_called_once_with(1)
    mock_item_dao.update_item.assert_called_once_with(sample_item)

    assert sample_item.name == "Updated Name"
    assert sample_item.price == 20.0
    assert sample_item.stock == 15
    assert sample_item.item_type == "TypeC"


def test_update_item_not_found(service: AdminMenuService, mock_item_dao: MagicMock):
    """Tests updating a non-existent item raises a ValueError."""
    mock_item_dao.find_item_by_id.return_value = None

    with pytest.raises(ValueError, match="No item found with ID 999."):
        service.update_item(999, "Updated Name", "Desc", 20.0, 15, True, "TypeC")


def test_update_item_validation_price(service: AdminMenuService, mock_item_dao: MagicMock, sample_item: Item):
    """Tests that updating an item with a negative price raises a ValueError."""
    mock_item_dao.find_item_by_id.return_value = sample_item

    with pytest.raises(ValueError, match="Price must be positive."):
        service.update_item(1, "Name", "Desc", -1.0, 10, True, "TypeA")


def test_update_item_validation_negative_stock(service: AdminMenuService, mock_item_dao: MagicMock, sample_item: Item):
    """Tests updating stock to a negative value."""
    mock_item_dao.find_item_by_id.return_value = sample_item
    with pytest.raises(ValueError, match="Stock cannot be negative."):
        service.update_item(1, stock=-5)


def test_update_item_validation_zero_stock_available(
    service: AdminMenuService, mock_item_dao: MagicMock, sample_item: Item
):
    """Tests updating stock to 0 while availability remains True."""
    sample_item.availability = True
    mock_item_dao.find_item_by_id.return_value = sample_item
    with pytest.raises(ValueError, match="Zero stock implies non-availability."):
        service.update_item(1, stock=0)


def test_update_item_dao_failure(service: AdminMenuService, mock_item_dao: MagicMock, sample_item: Item):
    """Tests that an Exception is raised if the DAO fails to update."""
    mock_item_dao.find_item_by_id.return_value = sample_item
    mock_item_dao.update_item.return_value = None

    with pytest.raises(Exception, match="Failed to update item: 1"):
        service.update_item(1, "Updated Name", "Desc", 20.0, 15, True, "TypeC")


def test_delete_item_success(service: AdminMenuService, mock_item_dao: MagicMock, sample_item: Item):
    """Tests successful deletion of an existing item."""
    mock_item_dao.find_item_by_id.return_value = sample_item
    mock_item_dao.delete_item.return_value = True

    service.delete_item(1)

    mock_item_dao.find_item_by_id.assert_called_once_with(1)
    mock_item_dao.delete_item.assert_called_once_with(1)


def test_delete_item_not_found(service: AdminMenuService, mock_item_dao: MagicMock):
    """Tests deleting a non-existent item raises a ValueError."""
    mock_item_dao.find_item_by_id.return_value = None

    with pytest.raises(ValueError, match="No item found with ID 999."):
        service.delete_item(999)


def test_delete_item_dao_failure(service: AdminMenuService, mock_item_dao: MagicMock, sample_item: Item):
    """Tests that an Exception is raised if the DAO fails to delete."""
    mock_item_dao.find_item_by_id.return_value = sample_item
    mock_item_dao.delete_item.return_value = False

    with pytest.raises(Exception, match="Failed to delete item: 1"):
        service.delete_item(1)


def test_list_items(service: AdminMenuService, mock_item_dao: MagicMock, sample_item_list: list):
    """Tests that list_items returns the list from the DAO."""
    mock_item_dao.find_all_items.return_value = sample_item_list

    result = service.list_items()

    assert result == sample_item_list
    mock_item_dao.find_all_items.assert_called_once()


def test_create_predefined_bundle_success(
    service: AdminMenuService, mock_bundle_dao: MagicMock, mock_item_dao: MagicMock, sample_item_list: list
):
    """Tests successful creation of a predefined bundle."""
    mock_item_dao.get_items_by_ids.return_value = sample_item_list
    mock_bundle_dao.add_predefined_bundle.return_value = MagicMock(spec=PredefinedBundle)

    item_ids = [1, 2]
    # CORRECTION: Suppression du paramètre `True` (availability)
    service.create_predefined_bundle("Menu Midi", "Desc", item_ids, 15.0)

    mock_item_dao.get_items_by_ids.assert_called_once_with(item_ids)
    mock_bundle_dao.add_predefined_bundle.assert_called_once_with(ANY)

    called_bundle = mock_bundle_dao.add_predefined_bundle.call_args[0][0]
    assert isinstance(called_bundle, PredefinedBundle)
    assert called_bundle.name == "Menu Midi"
    assert called_bundle.price == 15.0


def test_create_predefined_bundle_validation_price(service: AdminMenuService):
    """Tests that price <= 0 raises a ValueError."""
    with pytest.raises(ValueError, match="Price must be positive."):
        # CORRECTION: Suppression du paramètre `True`
        service.create_predefined_bundle("Bad Menu", "Desc", [1, 2], 0)


def test_create_predefined_bundle_validation_composition(service: AdminMenuService):
    """Tests that an empty composition raises a ValueError."""
    with pytest.raises(ValueError, match="Composition must contain at least 2 items."):
        # CORRECTION: Suppression du paramètre `True`
        service.create_predefined_bundle("Bad Menu", "Desc", [], 15.0)


def test_create_predefined_bundle_composition_mismatch(
    service: AdminMenuService, mock_item_dao: MagicMock, sample_item
):
    """Tests when one of the requested IDs is not found."""
    mock_item_dao.get_items_by_ids.return_value = [sample_item]
    with pytest.raises(ValueError, match="One or more item IDs provided in the composition were not found."):
        # CORRECTION: Suppression du paramètre `True`
        service.create_predefined_bundle("Menu", "Desc", [1, 99], 15.0)


def test_create_predefined_bundle_dao_failure(
    service: AdminMenuService, mock_bundle_dao: MagicMock, mock_item_dao: MagicMock, sample_item_list: list
):
    """Tests DAO failure during predefined bundle creation."""
    mock_item_dao.get_items_by_ids.return_value = sample_item_list
    mock_bundle_dao.add_predefined_bundle.return_value = None

    with pytest.raises(Exception, match="Failed to create predefined bundle: Menu Midi"):
        # CORRECTION: Suppression du paramètre `True`
        service.create_predefined_bundle("Menu Midi", "Desc", [1, 2], 15.0)


def test_update_predefined_bundle_success(
    service: AdminMenuService, mock_bundle_dao: MagicMock, mock_item_dao: MagicMock, sample_item_list: list
):
    """Tests successful update of a predefined bundle."""
    bundle = MagicMock(spec=PredefinedBundle)
    bundle.id_bundle = 1
    bundle.name = "Old"
    bundle.description = "Desc"
    bundle.price = 10.0
    bundle.composition = []

    mock_bundle_dao.find_bundle_by_id.return_value = bundle
    mock_item_dao.get_items_by_ids.return_value = sample_item_list
    mock_bundle_dao.update_bundle.return_value = True

    service.update_predefined_bundle(1, name="New Name", price=20.0, item_ids=[1, 2], description="")

    assert bundle.name == "New Name"
    assert bundle.price == 20.0
    assert bundle.composition == sample_item_list
    assert bundle.description == ""
    mock_bundle_dao.update_bundle.assert_called_once_with(bundle)


def test_update_predefined_bundle_not_found(service: AdminMenuService, mock_bundle_dao: MagicMock):
    """Tests updating a non-existent bundle raises a ValueError."""
    mock_bundle_dao.find_bundle_by_id.return_value = None
    with pytest.raises(ValueError, match="No bundle found with ID 999."):
        service.update_predefined_bundle(999)


def test_update_predefined_bundle_wrong_type(service: AdminMenuService, mock_bundle_dao: MagicMock):
    """Tests validation when trying to update a DiscountedBundle as a PredefinedBundle."""
    wrong_bundle = MagicMock(spec=DiscountedBundle)
    mock_bundle_dao.find_bundle_by_id.return_value = wrong_bundle
    with pytest.raises(TypeError, match="is not a predefined bundle"):
        service.update_predefined_bundle(1)


def test_update_predefined_bundle_price_missing(service: AdminMenuService, mock_bundle_dao: MagicMock):
    """Tests safety check for missing price attribute on existing bundle."""
    bundle = MagicMock(spec=PredefinedBundle)
    del bundle.price
    mock_bundle_dao.find_bundle_by_id.return_value = bundle
    with pytest.raises(Exception, match="Price is missing on existing bundle"):
        service.update_predefined_bundle(1, name="Test")


def test_update_predefined_bundle_negative_price(service: AdminMenuService, mock_bundle_dao: MagicMock):
    """Tests validation for negative price update."""
    bundle = MagicMock(spec=PredefinedBundle)
    bundle.price = 10.0
    mock_bundle_dao.find_bundle_by_id.return_value = bundle
    with pytest.raises(ValueError, match="Price must be positive"):
        service.update_predefined_bundle(1, price=-5.0)


def test_update_predefined_bundle_composition_error(
    service: AdminMenuService, mock_bundle_dao: MagicMock, mock_item_dao: MagicMock, sample_item
):
    """Tests invalid composition update (mismatch IDs)."""
    bundle = MagicMock(spec=PredefinedBundle)
    bundle.composition = []
    bundle.description = "Desc"
    bundle.price = 10.0

    mock_bundle_dao.find_bundle_by_id.return_value = bundle
    mock_item_dao.get_items_by_ids.return_value = [sample_item]
    with pytest.raises(ValueError, match="One or more item IDs provided in the composition were not found"):
        service.update_predefined_bundle(1, item_ids=[1, 99])


def test_update_predefined_bundle_dao_failure(service: AdminMenuService, mock_bundle_dao: MagicMock):
    """Tests DAO failure during predefined bundle update."""
    bundle = MagicMock(spec=PredefinedBundle)
    bundle.price = 10.0
    bundle.description = "Desc"  # <-- FIXED: Add required description attribute

    mock_bundle_dao.find_bundle_by_id.return_value = bundle
    mock_bundle_dao.update_bundle.return_value = False
    with pytest.raises(Exception, match="Failed to update predefined bundle"):
        service.update_predefined_bundle(1, name="Fail")


def test_create_discounted_bundle_success(
    service: AdminMenuService, mock_bundle_dao: MagicMock, sample_item_types: list
):
    """Tests successful creation of a discounted bundle with item types."""
    mock_bundle_dao.add_discounted_bundle.return_value = MagicMock(spec=DiscountedBundle)

    service.create_discounted_bundle("Menu Complet", "Desc", sample_item_types, 25.0)

    mock_bundle_dao.add_discounted_bundle.assert_called_once_with(ANY)

    called_bundle = mock_bundle_dao.add_discounted_bundle.call_args[0][0]
    assert isinstance(called_bundle, DiscountedBundle)
    assert called_bundle.name == "Menu Complet"
    assert called_bundle.discount == 25.0
    assert called_bundle.required_item_types == sample_item_types


def test_create_discounted_bundle_validation_discount_low(service: AdminMenuService, sample_item_types: list):
    """Tests that a discount <= 0 raises a ValueError."""
    with pytest.raises(ValueError, match="Discount must be between 0 and 100"):
        service.create_discounted_bundle("Bad Discount", "Desc", sample_item_types, 0)


def test_create_discounted_bundle_validation_discount_high(service: AdminMenuService, sample_item_types: list):
    """Tests that a discount >= 100 raises a ValueError."""
    with pytest.raises(ValueError, match="Discount must be between 0 and 100"):
        service.create_discounted_bundle("Bad Discount", "Desc", sample_item_types, 100)


def test_create_discounted_bundle_validation_item_types_empty(service: AdminMenuService):
    """Tests that an empty required_item_types list raises a ValueError."""
    with pytest.raises(ValueError, match="Item types cannot be empty."):
        service.create_discounted_bundle("Bad Discount", "Desc", [], 20.0)


def test_create_discounted_bundle_validation_invalid_strings(service: AdminMenuService):
    """Tests validation for empty or whitespace-only strings in item types."""
    with pytest.raises(ValueError, match="All item types must be valid, non-empty strings"):
        service.create_discounted_bundle("Bad", "Desc", ["Main", "  "], 20.0)


def test_create_discounted_bundle_dao_failure(
    service: AdminMenuService, mock_bundle_dao: MagicMock, sample_item_types: list
):
    """Tests DAO failure during discounted bundle creation."""
    mock_bundle_dao.add_discounted_bundle.return_value = None
    with pytest.raises(Exception, match="Failed to create discounted bundle"):
        service.create_discounted_bundle("Fail", "Desc", sample_item_types, 20.0)


def test_update_discounted_bundle_success(service: AdminMenuService, mock_bundle_dao: MagicMock):
    """Tests successful update of a discounted bundle."""
    bundle = DiscountedBundle(id_bundle=2, name="Old", description="Desc", discount=10, required_item_types=["a"])
    mock_bundle_dao.find_bundle_by_id.return_value = bundle
    mock_bundle_dao.update_bundle.return_value = True

    service.update_discounted_bundle(2, name="New", discount=15, required_item_types=["B", "C"])

    assert bundle.name == "New"
    assert bundle.discount == 15
    assert bundle.required_item_types == ["b", "c"]
    mock_bundle_dao.update_bundle.assert_called_once_with(bundle)


def test_update_discounted_bundle_not_found(service: AdminMenuService, mock_bundle_dao: MagicMock):
    """Tests updating a non-existent bundle raises a ValueError."""
    mock_bundle_dao.find_bundle_by_id.return_value = None
    with pytest.raises(ValueError, match="No bundle found with ID 999"):
        service.update_discounted_bundle(999)


def test_update_discounted_bundle_wrong_type(service: AdminMenuService, mock_bundle_dao: MagicMock):
    """Tests validation when trying to update a PredefinedBundle as a DiscountedBundle."""
    wrong_bundle = MagicMock(spec=PredefinedBundle)
    mock_bundle_dao.find_bundle_by_id.return_value = wrong_bundle
    with pytest.raises(TypeError, match="is not a discounted bundle"):
        service.update_discounted_bundle(2)


def test_update_discounted_bundle_invalid_discount(service: AdminMenuService, mock_bundle_dao: MagicMock):
    """Tests validation for invalid discount value update."""
    bundle = DiscountedBundle(id_bundle=2, name="Old", description="Desc", discount=10, required_item_types=["a"])
    mock_bundle_dao.find_bundle_by_id.return_value = bundle
    with pytest.raises(ValueError, match="Discount must be between 0 and 100"):
        service.update_discounted_bundle(2, discount=150)


def test_update_discounted_bundle_invalid_item_types(service: AdminMenuService, mock_bundle_dao: MagicMock):
    """Tests validation for invalid item types update."""
    bundle = DiscountedBundle(id_bundle=2, name="Old", description="Desc", discount=10, required_item_types=["a"])
    mock_bundle_dao.find_bundle_by_id.return_value = bundle
    with pytest.raises(ValueError, match="Item types cannot be empty"):
        service.update_discounted_bundle(2, required_item_types=[])


def test_update_discounted_bundle_dao_failure(service: AdminMenuService, mock_bundle_dao: MagicMock):
    """Tests DAO failure during discounted bundle update."""
    bundle = DiscountedBundle(id_bundle=2, name="Old", description="Desc", discount=10, required_item_types=["a"])
    mock_bundle_dao.find_bundle_by_id.return_value = bundle
    mock_bundle_dao.update_bundle.return_value = False
    with pytest.raises(Exception, match="Failed to update discounted bundle"):
        service.update_discounted_bundle(2, name="Fail")


def test_delete_bundle_success(service: AdminMenuService, mock_bundle_dao: MagicMock, sample_bundle: MagicMock):
    """Tests successful deletion of a bundle."""
    mock_bundle_dao.find_bundle_by_id.return_value = sample_bundle
    mock_bundle_dao.delete_bundle.return_value = True

    service.delete_bundle(5)

    mock_bundle_dao.find_bundle_by_id.assert_called_once_with(5)
    mock_bundle_dao.delete_bundle.assert_called_once_with(5)


def test_delete_bundle_not_found(service: AdminMenuService, mock_bundle_dao: MagicMock):
    """Tests deleting a non-existent bundle raises a ValueError."""
    mock_bundle_dao.find_bundle_by_id.return_value = None

    with pytest.raises(ValueError, match="No bundle found with ID 999."):
        service.delete_bundle(999)


def test_delete_bundle_dao_failure(service: AdminMenuService, mock_bundle_dao: MagicMock, sample_bundle: MagicMock):
    """Tests that an Exception is raised if the DAO fails to delete."""
    mock_bundle_dao.find_bundle_by_id.return_value = sample_bundle
    mock_bundle_dao.delete_bundle.return_value = False

    with pytest.raises(Exception, match="Failed to delete bundle: 5"):
        service.delete_bundle(5)


def test_list_bundles(service: AdminMenuService, mock_bundle_dao: MagicMock, sample_bundle: MagicMock):
    """Tests that list_bundles returns the list from the DAO."""
    mock_list = [sample_bundle, MagicMock(spec=AbstractBundle)]
    mock_bundle_dao.find_all_bundles.return_value = mock_list

    result = service.list_bundles()

    assert result == mock_list
    mock_bundle_dao.find_all_bundles.assert_called_once()