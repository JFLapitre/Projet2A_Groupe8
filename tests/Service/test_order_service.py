from datetime import datetime
from unittest.mock import ANY, MagicMock, patch

import pytest

from src.DAO.addressDAO import AddressDAO
from src.DAO.bundleDAO import BundleDAO
from src.DAO.DBConnector import DBConnector
from src.DAO.itemDAO import ItemDAO
from src.DAO.orderDAO import OrderDAO
from src.DAO.userDAO import UserDAO
from src.Model.abstract_bundle import AbstractBundle
from src.Model.address import Address
from src.Model.customer import Customer
from src.Model.driver import Driver
from src.Model.item import Item
from src.Model.order import Order
from src.Service.order_service import OrderService

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
def mock_user_dao():
    """Provides a mock UserDAO."""
    return MagicMock(spec=UserDAO)


@pytest.fixture
def mock_address_dao():
    """Provides a mock AddressDAO."""
    return MagicMock(spec=AddressDAO)


@pytest.fixture
def mock_bundle_dao():
    """Provides a mock BundleDAO."""
    return MagicMock(spec=BundleDAO)


@pytest.fixture
def mock_order_dao():
    """Provides a mock OrderDAO."""
    return MagicMock(spec=OrderDAO)


@pytest.fixture
def service(mock_db_connector, mock_item_dao, mock_user_dao, mock_address_dao, mock_bundle_dao, mock_order_dao, mocker):
    """
    Provides an OrderService instance with all DAO dependencies mocked.
    """
    # Patch all DAO constructors called within OrderService.__init__
    mocker.patch("src.Service.order_service.ItemDAO", return_value=mock_item_dao)
    mocker.patch("src.Service.order_service.UserDAO", return_value=mock_user_dao)
    mocker.patch("src.Service.order_service.AddressDAO", return_value=mock_address_dao)
    mocker.patch("src.Service.order_service.BundleDAO", return_value=mock_bundle_dao)
    mocker.patch("src.Service.order_service.OrderDAO", return_value=mock_order_dao)

    order_service = OrderService(db_connector=mock_db_connector)
    return order_service


# --- Data Fixtures ---


@pytest.fixture
def sample_customer():
    """Provides a mock Customer."""
    return MagicMock(spec=Customer, id=1, name="Test Customer")


@pytest.fixture
def sample_address():
    """Provides a mock Address."""
    return MagicMock(spec=Address, id=10, street="123 Test St")


@pytest.fixture
def sample_item_1():
    """Provides a mock Item, available with stock."""
    item = MagicMock(spec=Item)
    item.id_item = 1
    item.name = "Burger"
    item.availability = True
    item.stock = 10
    return item


@pytest.fixture
def sample_item_2():
    """Provides a second mock Item, available with stock."""
    item = MagicMock(spec=Item)
    item.id_item = 2
    item.name = "Fries"
    item.availability = True
    item.stock = 5
    return item


@pytest.fixture
def sample_item_unavailable():
    """Provides a mock Item that is UNAVAILABLE."""
    item = MagicMock(spec=Item)
    item.id_item = 3
    item.name = "Milkshake"
    item.availability = False
    item.stock = 0
    return item


@pytest.fixture
def sample_bundle_1(sample_item_1, sample_item_2):
    """Provides a mock Bundle with available items."""
    bundle = MagicMock(spec=AbstractBundle)
    bundle.id = 101
    bundle.name = "Menu 1"
    bundle.composition = [sample_item_1, sample_item_2]
    return bundle


@pytest.fixture
def sample_bundle_2(sample_item_1):
    """Provides a mock Bundle that uses the same item twice."""
    bundle = MagicMock(spec=AbstractBundle)
    bundle.id = 102
    bundle.name = "Double Burger"
    bundle.composition = [sample_item_1, sample_item_1]
    return bundle


@pytest.fixture
def sample_bundle_unavailable(sample_item_1, sample_item_unavailable):
    """Provides a mock Bundle with one unavailable item."""
    bundle = MagicMock(spec=AbstractBundle)
    bundle.id = 103
    bundle.name = "Broken Menu"
    bundle.composition = [sample_item_1, sample_item_unavailable]
    return bundle


@pytest.fixture
def sample_order_pending(sample_customer, sample_address):
    """Provides a mock 'pending' Order, starting empty."""
    order = MagicMock(spec=Order)
    order.id = 501
    order.customer = sample_customer
    order.address = sample_address
    order.status = "pending"
    # Note: MagicMock auto-creates attributes like 'bundles' as new mocks
    # We explicitly set it to a list for functions that append to it.
    order.bundles = []
    return order


@pytest.fixture
def sample_order_pending_with_bundle(sample_customer, sample_address, sample_bundle_1):
    """Provides a 'pending' order that already contains a bundle."""
    # This must be a deep copy or recreated if tests modify it
    bundle_list = [sample_bundle_1]
    order = MagicMock(spec=Order)
    order.id = 503
    order.customer = sample_customer
    order.address = sample_address
    order.status = "pending"
    order.bundles = bundle_list
    return order


@pytest.fixture
def sample_order_validated(sample_customer, sample_address, sample_bundle_1):
    """Provides a mock 'validated' Order."""
    order = MagicMock(spec=Order)
    order.id = 502
    order.customer = sample_customer
    order.address = sample_address
    order.status = "validated"
    order.bundles = [sample_bundle_1]
    return order


# --- Test Create Order ---


def test_create_order_success(
    service: OrderService,
    mock_user_dao: MagicMock,
    mock_address_dao: MagicMock,
    mock_order_dao: MagicMock,
    sample_customer: Customer,
    sample_address: Address,
    mocker,
):
    """Tests successful creation of a new, empty order."""
    mock_user_dao.find_user_by_id.return_value = sample_customer
    mock_address_dao.find_address_by_id.return_value = sample_address
    mock_created_order = MagicMock(spec=Order, id=1)
    mock_order_dao.add_order.return_value = mock_created_order
    mock_now = datetime(2025, 1, 1, 12, 0)
    mocker.patch("src.Service.order_service.datetime").now.return_value = mock_now

    result = service.create_order(customer_id=1, address_id=10)

    mock_user_dao.find_user_by_id.assert_called_once_with(1)
    mock_address_dao.find_address_by_id.assert_called_once_with(10)
    mock_order_dao.add_order.assert_called_once_with(ANY)

    called_order = mock_order_dao.add_order.call_args[0][0]
    assert isinstance(called_order, Order)
    assert called_order.customer == sample_customer
    assert called_order.address == sample_address
    assert called_order.status == "pending"
    assert called_order.bundles == []
    assert called_order.order_date == mock_now
    assert result == mock_created_order


def test_create_order_customer_not_found(service: OrderService, mock_user_dao: MagicMock):
    """Tests that a ValueError is raised if the customer is not found."""
    mock_user_dao.find_user_by_id.return_value = None
    with pytest.raises(ValueError, match="No valid customer found with ID 99"):
        service.create_order(customer_id=99, address_id=10)


def test_create_order_user_not_customer(service: OrderService, mock_user_dao: MagicMock):
    """Tests that a ValueError is raised if the user is not a Customer instance."""
    not_a_customer = MagicMock(spec=Driver)  # Is a User, but not a Customer
    mock_user_dao.find_user_by_id.return_value = not_a_customer
    with pytest.raises(ValueError, match="No valid customer found with ID 2"):
        service.create_order(customer_id=2, address_id=10)


def test_create_order_address_not_found(
    service: OrderService, mock_user_dao: MagicMock, mock_address_dao: MagicMock, sample_customer: Customer
):
    """Tests that a ValueError is raised if the address is not found."""
    mock_user_dao.find_user_by_id.return_value = sample_customer
    mock_address_dao.find_address_by_id.return_value = None
    with pytest.raises(ValueError, match="No address found with ID 99"):
        service.create_order(customer_id=1, address_id=99)


def test_create_order_dao_failure(
    service: OrderService,
    mock_user_dao: MagicMock,
    mock_address_dao: MagicMock,
    mock_order_dao: MagicMock,
    sample_customer: Customer,
    sample_address: Address,
):
    """Tests that an Exception is raised if the DAO fails to add the order."""
    mock_user_dao.find_user_by_id.return_value = sample_customer
    mock_address_dao.find_address_by_id.return_value = sample_address
    mock_order_dao.add_order.return_value = None

    with pytest.raises(Exception, match="Failed to create the order"):
        service.create_order(customer_id=1, address_id=10)


# --- Test Cancel Order ---


def test_cancel_order_success(service: OrderService, mock_order_dao: MagicMock, sample_order_pending: Order):
    """Tests successful cancellation (deletion) of an order."""
    mock_order_dao.find_order_by_id.return_value = sample_order_pending
    mock_order_dao.delete_order.return_value = True

    result = service.cancel_order(order_id=501)

    mock_order_dao.find_order_by_id.assert_called_once_with(501)
    mock_order_dao.delete_order.assert_called_once_with(501)
    assert result is True


def test_cancel_order_not_found(service: OrderService, mock_order_dao: MagicMock):
    """Tests that a ValueError is raised if the order to cancel is not found."""
    mock_order_dao.find_order_by_id.return_value = None

    with pytest.raises(ValueError, match="No order found with ID 99"):
        service.cancel_order(order_id=99)
    mock_order_dao.delete_order.assert_not_called()


def test_cancel_order_dao_failure(service: OrderService, mock_order_dao: MagicMock, sample_order_pending: Order):
    """Tests a failure in the DAO layer during deletion."""
    mock_order_dao.find_order_by_id.return_value = sample_order_pending
    mock_order_dao.delete_order.return_value = False  # Simulate DAO failure

    result = service.cancel_order(order_id=501)

    mock_order_dao.find_order_by_id.assert_called_once_with(501)
    mock_order_dao.delete_order.assert_called_once_with(501)
    assert result is False


# --- Test Add Bundle to Order ---
# These tests assume the BUG in the service is FIXED.
# They will FAIL until the 'add_bundle_to_order' logic is corrected.


def test_add_bundle_to_order_success(
    service: OrderService,
    mock_order_dao: MagicMock,
    mock_bundle_dao: MagicMock,
    sample_order_pending: Order,
    sample_bundle_1: AbstractBundle,
):
    """
    Tests adding a bundle with all available items to an order.
    """
    mock_order_dao.find_order_by_id.return_value = sample_order_pending
    mock_bundle_dao.find_bundle_by_id.return_value = sample_bundle_1
    mock_order_dao.update_order.return_value = sample_order_pending
    mock_order_dao.find_order_by_id.side_effect = [sample_order_pending, sample_order_pending]

    assert len(sample_order_pending.bundles) == 0

    result = service.add_bundle_to_order(order_id=501, bundle_id=101)

    assert len(sample_order_pending.bundles) == 1
    assert sample_order_pending.bundles[0] == sample_bundle_1
    mock_order_dao.update_order.assert_called_once_with(sample_order_pending)
    assert result == sample_order_pending


def test_add_bundle_to_order_item_not_available(
    service: OrderService,
    mock_order_dao: MagicMock,
    mock_bundle_dao: MagicMock,
    sample_order_pending: Order,
    sample_bundle_unavailable: AbstractBundle,
):
    """
    Tests that a ValueError is raised if one item in the bundle is unavailable.
    """
    mock_order_dao.find_order_by_id.return_value = sample_order_pending
    mock_bundle_dao.find_bundle_by_id.return_value = sample_bundle_unavailable

    with pytest.raises(ValueError, match="unavailable because items in the list '\\['Milkshake'\\]' are not available"):
        service.add_bundle_to_order(order_id=501, bundle_id=103)

    mock_order_dao.update_order.assert_not_called()
    assert len(sample_order_pending.bundles) == 0  # Bundle was not added


def test_add_bundle_to_order_order_not_found(service: OrderService, mock_order_dao: MagicMock):
    """Tests adding a bundle when the order is not found."""
    mock_order_dao.find_order_by_id.return_value = None
    with pytest.raises(ValueError, match="No order found with ID 99"):
        service.add_bundle_to_order(order_id=99, bundle_id=101)


def test_add_bundle_to_order_not_pending(
    service: OrderService, mock_order_dao: MagicMock, sample_order_validated: Order
):
    """Tests adding a bundle to an already validated order."""
    mock_order_dao.find_order_by_id.return_value = sample_order_validated
    with pytest.raises(ValueError, match="Cannot modify an order with status 'validated'"):
        service.add_bundle_to_order(order_id=502, bundle_id=101)


def test_add_bundle_to_order_bundle_not_found(
    service: OrderService, mock_order_dao: MagicMock, mock_bundle_dao: MagicMock, sample_order_pending: Order
):
    """Tests adding a bundle that does not exist."""
    mock_order_dao.find_order_by_id.return_value = sample_order_pending
    mock_bundle_dao.find_bundle_by_id.return_value = None
    with pytest.raises(ValueError, match="No bundle found with ID 99"):
        service.add_bundle_to_order(order_id=501, bundle_id=99)


def test_add_bundle_to_order_dao_failure(
    service: OrderService,
    mock_order_dao: MagicMock,
    mock_bundle_dao: MagicMock,
    sample_order_pending: Order,
    sample_bundle_1: AbstractBundle,
):
    """
    Tests an exception if the order update fails after adding the bundle.
    THIS TEST WILL FAIL UNTIL THE BUG IS FIXED.
    """
    mock_order_dao.find_order_by_id.return_value = sample_order_pending
    mock_bundle_dao.find_bundle_by_id.return_value = sample_bundle_1
    mock_order_dao.update_order.return_value = None  # Simulate DAO failure

    with pytest.raises(Exception, match="Failed to update the order"):
        service.add_bundle_to_order(order_id=501, bundle_id=101)

    assert len(sample_order_pending.bundles) == 1  # Bundle was added in memory...
    mock_order_dao.update_order.assert_called_once()  # ...but the update failed


# --- Test Validate Order ---


def test_validate_order_success_simple(
    service: OrderService,
    mock_order_dao: MagicMock,
    mock_item_dao: MagicMock,
    sample_order_pending_with_bundle: Order,
    sample_item_1: Item,
    sample_item_2: Item,
):
    """Tests successful validation of an order, checking stock reduction."""
    # Arrange: Order has bundle 1 (Item 1, Item 2)
    # Stocks are 10 and 5
    sample_item_1.stock = 10
    sample_item_2.stock = 5

    mock_order_dao.find_order_by_id.return_value = sample_order_pending_with_bundle
    # Mock find_item_by_id to return the correct item based on ID
    mock_item_dao.find_item_by_id.side_effect = (
        lambda id: sample_item_1 if id == 1 else (sample_item_2 if id == 2 else None)
    )

    mock_item_dao.update_item.return_value = True
    mock_order_dao.update_order.return_value = sample_order_pending_with_bundle

    # Act
    result = service.validate_order(order_id=503)

    # Assert
    # 1. Stock was reduced
    assert sample_item_1.stock == 9  # 10 - 1
    assert sample_item_2.stock == 4  # 5 - 1
    assert mock_item_dao.update_item.call_count == 2

    # 2. Order status was updated
    assert sample_order_pending_with_bundle.status == "validated"
    mock_order_dao.update_order.assert_called_once_with(sample_order_pending_with_bundle)
    assert result == sample_order_pending_with_bundle


def test_validate_order_success_complex_stock(
    service: OrderService,
    mock_order_dao: MagicMock,
    mock_item_dao: MagicMock,
    sample_item_1: Item,
    sample_item_2: Item,
    sample_bundle_1: AbstractBundle,
    sample_bundle_2: AbstractBundle,
):
    """Tests validation with multiple bundles and duplicate items."""
    # Arrange
    # Order needs: Bundle 1 (Item 1, Item 2) + Bundle 2 (Item 1, Item 1)
    # Total needed: Item 1 (x3), Item 2 (x1)
    sample_item_1.stock = 10
    sample_item_2.stock = 5

    complex_order = MagicMock(spec=Order, id=504, status="pending", bundles=[sample_bundle_1, sample_bundle_2])

    mock_order_dao.find_order_by_id.return_value = complex_order
    mock_item_dao.find_item_by_id.side_effect = (
        lambda id: sample_item_1 if id == 1 else (sample_item_2 if id == 2 else None)
    )
    mock_item_dao.update_item.return_value = True
    mock_order_dao.update_order.return_value = True

    # Act
    service.validate_order(order_id=504)

    # Assert
    assert sample_item_1.stock == 7  # 10 - 3
    assert sample_item_2.stock == 4  # 5 - 1
    assert mock_item_dao.update_item.call_count == 2

    assert complex_order.status == "validated"
    mock_order_dao.update_order.assert_called_once_with(complex_order)


def test_validate_order_stock_to_zero(
    service: OrderService,
    mock_order_dao: MagicMock,
    mock_item_dao: MagicMock,
    sample_order_pending_with_bundle: Order,
    sample_item_1: Item,
    sample_item_2: Item,
):
    """Tests that item availability is set to False when stock hits 0."""
    # Arrange: Order has bundle 1 (Item 1, Item 2)
    # Stocks are 1 and 1
    sample_item_1.stock = 1
    sample_item_1.availability = True
    sample_item_2.stock = 1
    sample_item_2.availability = True

    mock_order_dao.find_order_by_id.return_value = sample_order_pending_with_bundle
    mock_item_dao.find_item_by_id.side_effect = (
        lambda id: sample_item_1 if id == 1 else (sample_item_2 if id == 2 else None)
    )
    mock_item_dao.update_item.return_value = True
    mock_order_dao.update_order.return_value = True

    # Act
    service.validate_order(order_id=503)

    # Assert
    assert sample_item_1.stock == 0
    assert sample_item_1.availability is False  # Should be set to False
    assert sample_item_2.stock == 0
    assert sample_item_2.availability is False
    assert mock_item_dao.update_item.call_count == 2


def test_validate_order_not_enough_stock(
    service: OrderService,
    mock_order_dao: MagicMock,
    mock_item_dao: MagicMock,
    sample_order_pending_with_bundle: Order,
    sample_item_1: Item,
    sample_item_2: Item,
):
    """Tests that a ValueError is raised if stock is insufficient."""
    # Arrange: Order has bundle 1 (Item 1, Item 2)
    # Stocks are 10 and 0 (for item 2)
    sample_item_1.stock = 10
    sample_item_2.stock = 0

    mock_order_dao.find_order_by_id.return_value = sample_order_pending_with_bundle
    mock_item_dao.find_item_by_id.side_effect = (
        lambda id: sample_item_1 if id == 1 else (sample_item_2 if id == 2 else None)
    )

    # Act / Assert
    with pytest.raises(ValueError, match="Not enough stock for item 'Fries'. Needed: 1, Available: 0"):
        service.validate_order(order_id=503)

    mock_item_dao.update_item.assert_not_called()  # Should fail before any update
    mock_order_dao.update_order.assert_not_called()


def test_validate_order_item_not_found_in_db(
    service: OrderService,
    mock_order_dao: MagicMock,
    mock_item_dao: MagicMock,
    sample_order_pending_with_bundle: Order,
    sample_item_1: Item,
    sample_item_2: Item,
):
    """Tests that an Exception is raised if a required item no longer exists."""
    mock_order_dao.find_order_by_id.return_value = sample_order_pending_with_bundle
    # Item 2 returns None
    mock_item_dao.find_item_by_id.side_effect = lambda id: sample_item_1 if id == 1 else None

    with pytest.raises(Exception, match="Item ID 2 required for order no longer exists"):
        service.validate_order(order_id=503)

    mock_item_dao.update_item.assert_not_called()
    mock_order_dao.update_order.assert_not_called()


def test_validate_order_not_found(service: OrderService, mock_order_dao: MagicMock):
    """Tests validation on a non-existent order."""
    mock_order_dao.find_order_by_id.return_value = None
    with pytest.raises(ValueError, match="No order found with ID 99"):
        service.validate_order(order_id=99)


def test_validate_order_not_pending(service: OrderService, mock_order_dao: MagicMock, sample_order_validated: Order):
    """Tests validation on an already validated order."""
    mock_order_dao.find_order_by_id.return_value = sample_order_validated
    with pytest.raises(ValueError, match="Only 'pending' orders can be validated"):
        service.validate_order(order_id=502)


def test_validate_order_empty_order(service: OrderService, mock_order_dao: MagicMock, sample_order_pending: Order):
    """Tests validation on an order with no bundles."""
    mock_order_dao.find_order_by_id.return_value = sample_order_pending  # This order has bundles=[]
    with pytest.raises(ValueError, match="Cannot validate an empty order"):
        service.validate_order(order_id=501)


def test_validate_order_item_update_fails(
    service: OrderService,
    mock_order_dao: MagicMock,
    mock_item_dao: MagicMock,
    sample_order_pending_with_bundle: Order,
    sample_item_1: Item,
    sample_item_2: Item,
):
    """Tests that an Exception is raised if item stock update fails."""
    sample_item_1.stock = 10
    sample_item_2.stock = 5
    mock_order_dao.find_order_by_id.return_value = sample_order_pending_with_bundle
    mock_item_dao.find_item_by_id.side_effect = (
        lambda id: sample_item_1 if id == 1 else (sample_item_2 if id == 2 else None)
    )
    mock_item_dao.update_item.return_value = None  # Simulate DAO failure

    with pytest.raises(Exception, match="Failed to update stock for item 1. Validation aborted."):
        service.validate_order(order_id=503)

    mock_order_dao.update_order.assert_not_called()  # Should abort before this


def test_validate_order_status_update_fails(
    service: OrderService,
    mock_order_dao: MagicMock,
    mock_item_dao: MagicMock,
    sample_order_pending_with_bundle: Order,
    sample_item_1: Item,
    sample_item_2: Item,
):
    """Tests exception if stock updates but order status update fails."""
    sample_item_1.stock = 10
    sample_item_2.stock = 5
    mock_order_dao.find_order_by_id.return_value = sample_order_pending_with_bundle
    mock_item_dao.find_item_by_id.side_effect = (
        lambda id: sample_item_1 if id == 1 else (sample_item_2 if id == 2 else None)
    )
    mock_item_dao.update_item.return_value = True  # Stock updates succeed
    mock_order_dao.update_order.return_value = None  # Simulate DAO failure

    with pytest.raises(Exception, match="Stock was updated, but failed to validate the order status."):
        service.validate_order(order_id=503)

    assert mock_item_dao.update_item.call_count == 2  # Items were updated
    assert sample_order_pending_with_bundle.status == "validated"  # Status was set...
    mock_order_dao.update_order.assert_called_once()  # ...but DAO call failed


# --- Test Get/List Orders ---


def test_get_order_details_success(service: OrderService, mock_order_dao: MagicMock, sample_order_validated: Order):
    """Tests retrieving details for a single order."""
    mock_order_dao.find_order_by_id.return_value = sample_order_validated

    result = service.get_order_details(order_id=502)

    assert result == sample_order_validated
    mock_order_dao.find_order_by_id.assert_called_once_with(502)


def test_get_order_details_not_found(service: OrderService, mock_order_dao: MagicMock):
    """Tests retrieving a non-existent order."""
    mock_order_dao.find_order_by_id.return_value = None
    with pytest.raises(ValueError, match="No order found with ID 99"):
        service.get_order_details(order_id=99)


def test_list_orders_for_customer_success(
    service: OrderService,
    mock_user_dao: MagicMock,
    mock_order_dao: MagicMock,
    sample_customer: Customer,
    sample_order_validated: Order,
):
    """Tests retrieving the order history for a customer."""
    mock_user_dao.find_user_by_id.return_value = sample_customer
    order_list = [sample_order_validated, sample_order_pending_with_bundle]
    mock_order_dao.find_orders_by_customer.return_value = order_list

    result = service.list_orders_for_customer(customer_id=1)

    assert result == order_list
    mock_user_dao.find_user_by_id.assert_called_once_with(1)
    mock_order_dao.find_orders_by_customer.assert_called_once_with(1)


def test_list_orders_for_customer_no_orders(
    service: OrderService, mock_user_dao: MagicMock, mock_order_dao: MagicMock, sample_customer: Customer
):
    """Tests retrieving history for a customer with zero orders."""
    mock_user_dao.find_user_by_id.return_value = sample_customer
    mock_order_dao.find_orders_by_customer.return_value = []  # Empty list

    result = service.list_orders_for_customer(customer_id=1)

    assert result == []
    mock_order_dao.find_orders_by_customer.assert_called_once_with(1)


def test_list_orders_for_customer_not_found(service: OrderService, mock_user_dao: MagicMock):
    """Tests listing orders for a non-existent customer."""
    mock_user_dao.find_user_by_id.return_value = None
    with pytest.raises(ValueError, match="No valid customer found with ID 99"):
        service.list_orders_for_customer(customer_id=99)


def test_list_orders_for_customer_user_not_customer(service: OrderService, mock_user_dao: MagicMock):
    """Tests listing orders for a user ID that is not a customer."""
    not_a_customer = MagicMock(spec=Driver)
    mock_user_dao.find_user_by_id.return_value = not_a_customer
    with pytest.raises(ValueError, match="No valid customer found with ID 99"):
        service.list_orders_for_customer(customer_id=99)
