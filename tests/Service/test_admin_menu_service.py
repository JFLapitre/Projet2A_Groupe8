from unittest.mock import ANY, MagicMock, patch

import pytest

from src.DAO.bundleDAO import BundleDAO
from src.DAO.DBConnector import DBConnector
from src.DAO.itemDAO import ItemDAO
from src.Model.abstract_bundle import AbstractBundle
from src.Model.discounted_bundle import DiscountedBundle
from src.Model.item import Item
from src.Model.one_item_bundle import OneItemBundle
from src.Model.predefined_bundle import PredefinedBundle
from src.Service.admin_menu_service import AdminMenuService

# --- Fixtures ---


@pytest.fixture
def mock_db_connector():
    """Provides a mock DBConnector."""
    return MagicMock(spec=DBConnector)


@pytest.fixture
def mock_item_dao():
    """Provides a mock ItemDAO."""
    return MagicMock(spec=ItemDAO)


@pytest.fixture
def mock_bundle_dao():
    """Provides a mock BundleDAO."""
    return MagicMock(spec=BundleDAO)


@pytest.fixture
def service(mock_db_connector, mock_item_dao, mock_bundle_dao, mocker):
    """
    Provides an AdminMenuService instance with mocked DAOs.
    It patches the DAO constructors to inject our mocks when the service is initialized.
    """
    # Patch the *constructors* within the module where they are called (admin_menu_service)
    mocker.patch("src.Service.admin_menu_service.ItemDAO", return_value=mock_item_dao)
    mocker.patch("src.Service.admin_menu_service.BundleDAO", return_value=mock_bundle_dao)

    # Now, when AdminMenuService is created, it will receive the mocks
    admin_service = AdminMenuService(db_connector=mock_db_connector)
    return admin_service


@pytest.fixture
def sample_item():
    """Provides a reusable sample Item for tests."""
    return Item(id=1, name="Test Item", description="Desc", price=10.0, stock=5, availability=True, item_type="TypeA")


@pytest.fixture
def sample_item_list(sample_item):
    """Provides a reusable list of Items for bundle compositions."""
    item2 = Item(
        id=2, name="Test Item 2", description="Desc 2", price=20.0, stock=10, availability=True, item_type="TypeB"
    )
    return [sample_item, item2]


@pytest.fixture
def sample_bundle():
    """Provides a mock bundle for deletion/find tests."""
    return MagicMock(spec=AbstractBundle)


# --- Item Function Tests ---


def test_create_item_success(service: AdminMenuService, mock_item_dao: MagicMock):
    """Tests successful creation of a valid item."""
    mock_item_dao.add_item.return_value = MagicMock(spec=Item) 

    service.create_item("New Item", "Desc", 15.0, 10, True, "TypeB")

    # Check that the DAO was called with an Item object
    mock_item_dao.add_item.assert_called_once_with(ANY)

    # Check attributes of the object passed to the DAO
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
    mock_item_dao.add_item.return_value = None  # Simulate DAO failure

    with pytest.raises(Exception, match="Failed to create item: New Item"):
        service.create_item("New Item", "Desc", 15.0, 10, True, "TypeB")


def test_update_item_success(service: AdminMenuService, mock_item_dao: MagicMock, sample_item: Item):
    """Tests successful update of an existing item."""
    mock_item_dao.find_item_by_id.return_value = sample_item
    mock_item_dao.update_item.return_value = sample_item

    service.update_item(1, "Updated Name", "Updated Desc", 20.0, 15, True, "TypeC")

    mock_item_dao.find_item_by_id.assert_called_once_with(1)
    mock_item_dao.update_item.assert_called_once_with(sample_item)

    # Check that the service modified the item *before* calling update_item
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


def test_update_item_dao_failure(service: AdminMenuService, mock_item_dao: MagicMock, sample_item: Item):
    """Tests that an Exception is raised if the DAO fails to update."""
    mock_item_dao.find_item_by_id.return_value = sample_item
    mock_item_dao.update_item.return_value = None  # Simulate DAO failure

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
    mock_item_dao.delete_item.return_value = False  # Simulate DAO failure

    with pytest.raises(Exception, match="Failed to delete item: 1"):
        service.delete_item(1)


def test_list_items(service: AdminMenuService, mock_item_dao: MagicMock, sample_item_list: list):
    """Tests that list_items returns the list from the DAO."""
    mock_item_dao.find_all_items.return_value = sample_item_list

    result = service.list_items()

    assert result == sample_item_list
    mock_item_dao.find_all_items.assert_called_once()


# --- Bundle Function Tests ---


def test_create_predefined_bundle_success(
    service: AdminMenuService, mock_bundle_dao: MagicMock, sample_item_list: list
):
    """Tests successful creation of a predefined bundle."""
    mock_bundle_dao.add_predefined_bundle.return_value = MagicMock(spec=PredefinedBundle)

    service.create_predefined_bundle("Menu Midi", "Desc", sample_item_list, True, 15.0)

    mock_bundle_dao.add_predefined_bundle.assert_called_once_with(ANY)
    called_bundle = mock_bundle_dao.add_predefined_bundle.call_args[0][0]
    assert isinstance(called_bundle, PredefinedBundle)
    assert called_bundle.name == "Menu Midi"
    assert called_bundle.price == 15.0


def test_create_predefined_bundle_validation_price(service: AdminMenuService, sample_item_list: list):
    """Tests that price <= 0 raises a ValueError."""
    with pytest.raises(ValueError, match="Price must be positive."):
        service.create_predefined_bundle("Bad Menu", "Desc", sample_item_list, True, 0)


def test_create_predefined_bundle_validation_composition(service: AdminMenuService):
    """Tests that an empty composition raises a ValueError."""
    with pytest.raises(ValueError, match="Composition cannot be empty."):
        service.create_predefined_bundle("Bad Menu", "Desc", [], True, 15.0)


def test_create_predefined_bundle_dao_failure(
    service: AdminMenuService, mock_bundle_dao: MagicMock, sample_item_list: list
):
    """Tests DAO failure during predefined bundle creation."""
    mock_bundle_dao.add_predefined_bundle.return_value = None

    with pytest.raises(Exception, match="Failed to create predefined bundle: Menu Midi"):
        service.create_predefined_bundle("Menu Midi", "Desc", sample_item_list, True, 15.0)


def test_create_one_item_bundle_success(service: AdminMenuService, mock_bundle_dao: MagicMock, sample_item: Item):
    """Tests successful creation of a one-item bundle."""
    mock_bundle_dao.add_one_item_bundle.return_value = MagicMock(spec=OneItemBundle)

    service.create_one_item_bundle("Solo Deal", "Desc", 8.0, sample_item)

    mock_bundle_dao.add_one_item_bundle.assert_called_once_with(ANY)
    called_bundle = mock_bundle_dao.add_one_item_bundle.call_args[0][0]
    assert isinstance(called_bundle, OneItemBundle)
    assert called_bundle.name == "Solo Deal"
    assert called_bundle.composition == [sample_item]


def test_create_one_item_bundle_validation_price(service: AdminMenuService, sample_item: Item):
    """Tests that price <= 0 raises a ValueError."""
    with pytest.raises(ValueError, match="Price must be positive."):
        service.create_one_item_bundle("Bad Deal", "Desc", 0, sample_item)


def test_create_one_item_bundle_validation_item(service: AdminMenuService):
    """Tests that a null item raises a ValueError."""
    with pytest.raises(ValueError, match="Item cannot be null."):
        service.create_one_item_bundle("Bad Deal", "Desc", 8.0, None)


def test_create_discounted_bundle_success(
    service: AdminMenuService, mock_bundle_dao: MagicMock, sample_item_list: list
):
    """Tests successful creation of a discounted bundle."""
    mock_bundle_dao.add_discounted_bundle.return_value = MagicMock(spec=DiscountedBundle)

    service.create_discounted_bundle("Happy Hour", "Desc", sample_item_list, 20.0)

    mock_bundle_dao.add_discounted_bundle.assert_called_once_with(ANY)
    called_bundle = mock_bundle_dao.add_discounted_bundle.call_args[0][0]
    assert isinstance(called_bundle, DiscountedBundle)
    assert called_bundle.name == "Happy Hour"
    assert called_bundle.discount == 20.0


def test_create_discounted_bundle_validation_discount_low(service: AdminMenuService, sample_item_list: list):
    """Tests that a discount <= 0 raises a ValueError."""
    with pytest.raises(ValueError, match="Discount must be between 0 and 100"):
        service.create_discounted_bundle("Bad Discount", "Desc", sample_item_list, 0)


def test_create_discounted_bundle_validation_discount_high(service: AdminMenuService, sample_item_list: list):
    """Tests that a discount >= 100 raises a ValueError."""
    with pytest.raises(ValueError, match="Discount must be between 0 and 100"):
        service.create_discounted_bundle("Bad Discount", "Desc", sample_item_list, 100)


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
    mock_bundle_dao.delete_bundle.return_value = False  # Simulate DAO failure

    with pytest.raises(Exception, match="Failed to delete bundle: 5"):
        service.delete_bundle(5)


def test_list_bundles(service: AdminMenuService, mock_bundle_dao: MagicMock, sample_bundle: MagicMock):
    """Tests that list_bundles returns the list from the DAO."""
    mock_list = [sample_bundle, MagicMock(spec=AbstractBundle)]
    mock_bundle_dao.find_all_bundles.return_value = mock_list

    result = service.list_bundles()

    assert result == mock_list
    mock_bundle_dao.find_all_bundles.assert_called_once()
