from datetime import datetime
from unittest.mock import ANY, MagicMock

import pytest

from src.DAO.addressDAO import AddressDAO
from src.DAO.bundleDAO import BundleDAO
from src.DAO.DBConnector import DBConnector
from src.DAO.deliveryDAO import DeliveryDAO
from src.DAO.itemDAO import ItemDAO
from src.DAO.orderDAO import OrderDAO
from src.DAO.userDAO import UserDAO
from src.Model.customer import Customer
from src.Model.delivery import Delivery
from src.Model.driver import Driver
from src.Model.order import Order
from src.Service.driver_service import DriverService

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
def mock_delivery_dao():
    """Provides a mock DeliveryDAO."""
    return MagicMock(spec=DeliveryDAO)


@pytest.fixture
def service(
    mock_db_connector,
    mock_item_dao,
    mock_user_dao,
    mock_address_dao,
    mock_bundle_dao,
    mock_order_dao,
    mock_delivery_dao,
    mocker,
):
    """
    Provides a DriverService instance with all DAO dependencies mocked.
    This is complex due to the chained __init__ in the service.
    """
    mocker.patch("src.Service.driver_service.ItemDAO", return_value=mock_item_dao)
    mocker.patch("src.Service.driver_service.UserDAO", return_value=mock_user_dao)
    mocker.patch("src.Service.driver_service.AddressDAO", return_value=mock_address_dao)
    mocker.patch("src.Service.driver_service.BundleDAO", return_value=mock_bundle_dao)
    mocker.patch("src.Service.driver_service.OrderDAO", return_value=mock_order_dao)
    mocker.patch("src.Service.driver_service.DeliveryDAO", return_value=mock_delivery_dao)

    # Now, create the service. Its __init__ will use all the mocks above.
    driver_service = DriverService(db_connector=mock_db_connector)
    return driver_service


@pytest.fixture
def sample_driver_available():
    """Provides a mock Driver who is available."""
    driver = MagicMock(spec=Driver)
    driver.id = 1
    driver.name = "Test Driver"
    driver.availability = True
    return driver


@pytest.fixture
def sample_driver_unavailable():
    """Provides a mock Driver who is not available."""
    driver = MagicMock(spec=Driver)
    driver.id = 2
    driver.name = "Busy Driver"
    driver.availability = False
    return driver


@pytest.fixture
def sample_order_validated():
    """Provides a mock Order with 'validated' status."""
    order = MagicMock(spec=Order)
    order.id = 101
    order.status = "validated"
    return order


@pytest.fixture
def sample_order_pending():
    """Provides a mock Order with 'pending' status."""
    order = MagicMock(spec=Order)
    order.id = 102
    order.status = "pending"
    return order


@pytest.fixture
def sample_delivery_inprogress(sample_driver_available, sample_order_validated):
    """Provides a mock Delivery with 'in_progress' status."""
    delivery = MagicMock(spec=Delivery)
    delivery.id = 50
    delivery.driver = sample_driver_available
    delivery.orders = [sample_order_validated]
    delivery.status = "in_progress"
    delivery.delivery_time = None
    return delivery


@pytest.fixture
def sample_delivery_pending():
    """Provides a mock Delivery with 'pending' status."""
    delivery = MagicMock(spec=Delivery)
    delivery.id = 51
    delivery.status = "pending"
    return delivery


# --- Test Create and Assign Delivery ---


def test_create_and_assign_delivery_success(
    service: DriverService,
    mock_user_dao: MagicMock,
    mock_order_dao: MagicMock,
    mock_delivery_dao: MagicMock,
    sample_driver_available: Driver,
    sample_order_validated: Order,
):
    """Tests successful creation and assignment of a new delivery."""
    # Arrange
    mock_user_dao.find_user_by_id.return_value = sample_driver_available
    mock_order_dao.find_order_by_id.return_value = sample_order_validated

    mock_created_delivery = MagicMock(spec=Delivery, id=1)
    mock_delivery_dao.add_delivery.return_value = mock_created_delivery

    order_ids = [sample_order_validated.id]
    driver_id = sample_driver_available.id

    # Act
    result = service.create_and_assign_delivery(order_ids, driver_id)

    # Assert
    mock_user_dao.find_user_by_id.assert_called_once_with(driver_id)
    mock_order_dao.find_order_by_id.assert_called_once_with(sample_order_validated.id)

    # Check the object passed to add_delivery
    mock_delivery_dao.add_delivery.assert_called_once_with(ANY)
    called_delivery = mock_delivery_dao.add_delivery.call_args[0][0]
    assert isinstance(called_delivery, Delivery)
    assert called_delivery.driver == sample_driver_available
    assert called_delivery.orders == [sample_order_validated]
    assert called_delivery.status == "in_progress"

    assert result == mock_created_delivery


def test_create_delivery_validation_no_orders(service: DriverService):
    """Tests that a ValueError is raised if order_ids is empty."""
    with pytest.raises(ValueError, match="Cannot create a delivery with no orders."):
        service.create_and_assign_delivery(order_ids=[], driver_id=1)


def test_create_delivery_validation_driver_not_found(service: DriverService, mock_user_dao: MagicMock):
    """Tests that a ValueError is raised if the driver is not found."""
    mock_user_dao.find_user_by_id.return_value = None
    with pytest.raises(ValueError, match="No valid driver found with ID 999"):
        service.create_and_assign_delivery(order_ids=[101], driver_id=999)


def test_create_delivery_validation_user_is_not_driver(service: DriverService, mock_user_dao: MagicMock):
    """Tests that a ValueError is raised if the found user is not a Driver instance."""
    not_a_driver = MagicMock(spec=Customer)  # Is a User, but not a Driver
    mock_user_dao.find_user_by_id.return_value = not_a_driver
    with pytest.raises(ValueError, match="No valid driver found with ID 3"):
        service.create_and_assign_delivery(order_ids=[101], driver_id=3)


def test_create_delivery_validation_driver_not_available(
    service: DriverService, mock_user_dao: MagicMock, sample_driver_unavailable: Driver
):
    """Tests that a ValueError is raised if the driver is not available."""
    mock_user_dao.find_user_by_id.return_value = sample_driver_unavailable
    with pytest.raises(ValueError, match="is not available"):
        service.create_and_assign_delivery(order_ids=[101], driver_id=sample_driver_unavailable.id)


def test_create_delivery_validation_order_not_found(
    service: DriverService, mock_user_dao: MagicMock, mock_order_dao: MagicMock, sample_driver_available: Driver
):
    """Tests that a ValueError is raised if an order is not found."""
    mock_user_dao.find_user_by_id.return_value = sample_driver_available
    mock_order_dao.find_order_by_id.return_value = None
    with pytest.raises(ValueError, match="Order with ID 999 not found"):
        service.create_and_assign_delivery(order_ids=[999], driver_id=sample_driver_available.id)


def test_create_delivery_validation_order_not_validated(
    service: DriverService,
    mock_user_dao: MagicMock,
    mock_order_dao: MagicMock,
    sample_driver_available: Driver,
    sample_order_pending: Order,
):
    """Tests that a ValueError is raised if an order is not in 'validated' status."""
    mock_user_dao.find_user_by_id.return_value = sample_driver_available
    mock_order_dao.find_order_by_id.return_value = sample_order_pending
    with pytest.raises(ValueError, match="is not validated"):
        service.create_and_assign_delivery(order_ids=[sample_order_pending.id], driver_id=sample_driver_available.id)


def test_create_delivery_dao_failure(
    service: DriverService,
    mock_user_dao: MagicMock,
    mock_order_dao: MagicMock,
    mock_delivery_dao: MagicMock,
    sample_driver_available: Driver,
    sample_order_validated: Order,
):
    """Tests that an Exception is raised if the DAO fails to add the delivery."""
    mock_user_dao.find_user_by_id.return_value = sample_driver_available
    mock_order_dao.find_order_by_id.return_value = sample_order_validated
    mock_delivery_dao.add_delivery.return_value = None  # Simulate DAO failure

    with pytest.raises(Exception, match="Failed to create and assign the delivery"):
        service.create_and_assign_delivery(order_ids=[101], driver_id=1)


# --- Test Complete Delivery ---


def test_complete_delivery_success(
    service: DriverService,
    mock_delivery_dao: MagicMock,
    mock_order_dao: MagicMock,
    sample_delivery_inprogress: Delivery,
    mocker,
):
    """Tests successful completion of an 'in_progress' delivery."""
    # Arrange
    mock_delivery_dao.find_delivery_by_id.return_value = sample_delivery_inprogress
    mock_delivery_dao.update_delivery.return_value = sample_delivery_inprogress

    # Mock datetime.now()
    mock_now = datetime(2025, 11, 5, 12, 30, 0)
    mocker.patch("src.Service.driver_service.datetime").now.return_value = mock_now

    # Act
    result = service.complete_delivery(sample_delivery_inprogress.id)

    # Assert
    mock_delivery_dao.find_delivery_by_id.assert_called_once_with(sample_delivery_inprogress.id)

    # Check that the delivery object was modified
    assert sample_delivery_inprogress.status == "completed"
    assert sample_delivery_inprogress.delivery_time == mock_now

    # Check that orders were updated
    for order in sample_delivery_inprogress.orders:
        assert order.status == "delivered"
        mock_order_dao.update_order.assert_called_with(order)

    mock_delivery_dao.update_delivery.assert_called_once_with(sample_delivery_inprogress)
    assert result == sample_delivery_inprogress


def test_complete_delivery_validation_not_found(service: DriverService, mock_delivery_dao: MagicMock):
    """Tests that a ValueError is raised if the delivery is not found."""
    mock_delivery_dao.find_delivery_by_id.return_value = None
    with pytest.raises(ValueError, match="No delivery found with ID 999"):
        service.complete_delivery(999)


def test_complete_delivery_validation_wrong_status(
    service: DriverService, mock_delivery_dao: MagicMock, sample_delivery_pending: Delivery
):
    """Tests that a ValueError is raised if the delivery is not 'in_progress'."""
    mock_delivery_dao.find_delivery_by_id.return_value = sample_delivery_pending
    with pytest.raises(ValueError, match="Only 'in_progress' deliveries can be completed"):
        service.complete_delivery(sample_delivery_pending.id)


def test_complete_delivery_order_update_fails(
    service: DriverService,
    mock_delivery_dao: MagicMock,
    mock_order_dao: MagicMock,
    sample_delivery_inprogress: Delivery,
    caplog,  # Pytest fixture to capture logs
):
    """
    Tests that the delivery is still completed even if an order update fails.
    The service should log this warning but not crash.
    """
    # Arrange
    mock_delivery_dao.find_delivery_by_id.return_value = sample_delivery_inprogress
    mock_delivery_dao.update_delivery.return_value = sample_delivery_inprogress
    mock_order_dao.update_order.side_effect = Exception("DB Error")  # Simulate order update failure

    # Act
    result = service.complete_delivery(sample_delivery_inprogress.id)

    # Assert
    # Check that the log was written
    assert "Could not update status for orders" in caplog.text

    # Check that the delivery *was* still updated and completed
    assert sample_delivery_inprogress.status == "completed"
    mock_delivery_dao.update_delivery.assert_called_once_with(sample_delivery_inprogress)
    assert result == sample_delivery_inprogress


def test_complete_delivery_dao_failure(
    service: DriverService, mock_delivery_dao: MagicMock, sample_delivery_inprogress: Delivery
):
    """Tests that an Exception is raised if the delivery update fails."""
    mock_delivery_dao.find_delivery_by_id.return_value = sample_delivery_inprogress
    mock_delivery_dao.update_delivery.return_value = None  # Simulate DAO failure

    with pytest.raises(Exception, match="Failed to update delivery status to completed"):
        service.complete_delivery(sample_delivery_inprogress.id)


# --- Test Get Delivery Details ---


def test_get_delivery_details_success(
    service: DriverService, mock_delivery_dao: MagicMock, sample_delivery_inprogress: Delivery
):
    """Tests that details for a specific delivery are returned."""
    mock_delivery_dao.find_delivery_by_id.return_value = sample_delivery_inprogress

    result = service.get_delivery_details(sample_delivery_inprogress.id)

    assert result == sample_delivery_inprogress
    mock_delivery_dao.find_delivery_by_id.assert_called_once_with(sample_delivery_inprogress.id)


def test_get_delivery_details_not_found(service: DriverService, mock_delivery_dao: MagicMock):
    """Tests that a ValueError is raised if the delivery is not found."""
    mock_delivery_dao.find_delivery_by_id.return_value = None

    with pytest.raises(ValueError, match="No delivery found with ID 999"):
        service.get_delivery_details(999)


# --- Test List Pending Deliveries ---


def test_list_pending_deliveries_success(
    service: DriverService,
    mock_delivery_dao: MagicMock,
    sample_delivery_pending: Delivery,
    sample_delivery_inprogress: Delivery,
):
    """Tests that only deliveries with 'pending' status are returned."""
    all_deliveries = [sample_delivery_pending, sample_delivery_inprogress]
    mock_delivery_dao.find_all_deliveries.return_value = all_deliveries

    result = service.list_pending_deliveries()

    assert result == [sample_delivery_pending]
    mock_delivery_dao.find_all_deliveries.assert_called_once()


def test_list_pending_deliveries_empty(service: DriverService, mock_delivery_dao: MagicMock):
    """Tests that an empty list is returned if no deliveries exist."""
    mock_delivery_dao.find_all_deliveries.return_value = []

    result = service.list_pending_deliveries()

    assert result == []
