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
from src.Model.address import Address
from src.Model.customer import Customer
from src.Model.delivery import Delivery
from src.Model.driver import Driver
from src.Model.order import Order
from src.Service.api_maps_service import ApiMapsService
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
    """
    # Patch all DAO constructors called within DriverService.__init__
    mocker.patch("src.Service.driver_service.ItemDAO", return_value=mock_item_dao)
    mocker.patch("src.Service.driver_service.UserDAO", return_value=mock_user_dao)
    mocker.patch("src.Service.driver_service.AddressDAO", return_value=mock_address_dao)
    mocker.patch("src.Service.driver_service.BundleDAO", return_value=mock_bundle_dao)
    mocker.patch("src.Service.driver_service.OrderDAO", return_value=mock_order_dao)
    mocker.patch("src.Service.driver_service.DeliveryDAO", return_value=mock_delivery_dao)

    # Mock ApiMapsService pour get_itinerary
    mocker.patch("src.Service.driver_service.ApiMapsService")

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
def sample_customer():
    """Provides a mock Customer with an ID and name."""
    customer = MagicMock(spec=Customer)
    customer.id = 10
    customer.name = "Test Customer"
    return customer


@pytest.fixture
def sample_address():
    """Provides a mock Address with details."""
    address = MagicMock(spec=Address)
    address.street_number = "123"
    address.street_name = "Main St"
    address.city = "Testville"
    return address


@pytest.fixture
def sample_order_pending(sample_customer, sample_address):
    """Provides a mock Order with 'pending' status."""
    order = MagicMock(spec=Order)
    order.id = 101
    order.status = "pending"
    order.customer = sample_customer
    order.address = sample_address
    order.id_order = 101  # <--- AJOUTEZ CETTE LIGNE
    return order


@pytest.fixture
def sample_order_validated(sample_customer, sample_address):
    """Provides a mock Order with 'validated' status (used to ensure test fails against service)."""
    order = MagicMock(spec=Order)
    order.id = 102
    order.status = "validated"
    order.customer = sample_customer
    order.address = sample_address
    return order


@pytest.fixture
def sample_delivery_inprogress(sample_driver_available, sample_order_pending):
    """Provides a mock Delivery with 'in_progress' status, linked to a pending order."""
    delivery = MagicMock(spec=Delivery)
    delivery.id = 50
    delivery.driver = sample_driver_available
    # Le service change le statut de la commande en in_progress lors de la création de la livraison
    delivery.orders = [sample_order_pending]
    delivery.status = "in_progress"
    delivery.delivery_time = None
    return delivery


@pytest.fixture
def sample_delivery_pending():
    """Provides a mock Delivery with 'pending' status (should be filtered out)."""
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
    sample_order_pending: Order,  # CHANGEMENT: Utiliser pending
    mocker,
):
    """Tests successful creation and assignment of a new delivery."""
    # Arrange
    mock_user_dao.find_user_by_id.return_value = sample_driver_available
    mock_order_dao.find_order_by_id.return_value = sample_order_pending

    mock_created_delivery = MagicMock(spec=Delivery, id=1)
    mock_delivery_dao.add_delivery.return_value = mock_created_delivery
    mock_order_dao.update_order.return_value = True
    mock_user_dao.update_user.return_value = True

    order_ids = [sample_order_pending.id]
    driver_id = sample_driver_available.id

    # Act
    result = service.create_and_assign_delivery(order_ids, driver_id)

    # Assert
    mock_user_dao.find_user_by_id.assert_called_once_with(driver_id)
    mock_order_dao.find_order_by_id.assert_called_once_with(sample_order_pending.id)

    # Vérification que le statut de la commande a été mis à jour
    assert sample_order_pending.status == "in_progress"
    mock_order_dao.update_order.assert_called_once_with(sample_order_pending)

    # Vérification que la disponibilité du chauffeur a été mise à jour
    assert sample_driver_available.availability is False
    mock_user_dao.update_user.assert_called_once_with(sample_driver_available)

    # Vérification de l'objet passé à add_delivery
    mock_delivery_dao.add_delivery.assert_called_once_with(ANY)
    called_delivery = mock_delivery_dao.add_delivery.call_args[0][0]
    assert isinstance(called_delivery, Delivery)
    assert called_delivery.driver == sample_driver_available
    assert called_delivery.orders == [sample_order_pending]
    assert called_delivery.status == "in_progress"

    assert result == mock_created_delivery


def test_create_delivery_validation_no_orders(service: DriverService):
    """Tests that a ValueError is raised if order_ids is empty."""
    with pytest.raises(ValueError, match="Cannot create a delivery with no orders."):
        service.create_and_assign_delivery(order_ids=[], user_id=1)


def test_create_delivery_validation_driver_not_found(service: DriverService, mock_user_dao: MagicMock):
    """Tests that a ValueError is raised if the driver is not found."""
    mock_user_dao.find_user_by_id.return_value = None
    with pytest.raises(ValueError, match="No valid driver found with ID 999"):
        service.create_and_assign_delivery(order_ids=[101], user_id=999)


def test_create_delivery_validation_user_is_not_driver(service: DriverService, mock_user_dao: MagicMock):
    """Tests that a ValueError is raised if the found user is not a Driver instance."""
    not_a_driver = MagicMock(spec=Customer)  # Is a User, but not a Driver
    mock_user_dao.find_user_by_id.return_value = not_a_driver
    with pytest.raises(ValueError, match="No valid driver found with ID 3"):
        service.create_and_assign_delivery(order_ids=[101], user_id=3)


def test_create_delivery_validation_driver_not_available(
    service: DriverService, mock_user_dao: MagicMock, sample_driver_unavailable: Driver
):
    """Tests that a ValueError is raised if the driver is not available."""
    mock_user_dao.find_user_by_id.return_value = sample_driver_unavailable
    with pytest.raises(ValueError, match="is not available to start a new delivery."):
        service.create_and_assign_delivery(order_ids=[101], user_id=sample_driver_unavailable.id)


def test_create_delivery_validation_order_not_found(
    service: DriverService, mock_user_dao: MagicMock, mock_order_dao: MagicMock, sample_driver_available: Driver
):
    """Tests that a ValueError is raised if an order is not found."""
    mock_user_dao.find_user_by_id.return_value = sample_driver_available
    mock_order_dao.find_order_by_id.return_value = None
    with pytest.raises(ValueError, match="Order with ID 999 not found."):
        service.create_and_assign_delivery(order_ids=[999], user_id=sample_driver_available.id)


def test_create_delivery_validation_order_not_pending(  # CHANGEMENT: le statut est maintenant "pending" dans le service
    service: DriverService,
    mock_user_dao: MagicMock,
    mock_order_dao: MagicMock,
    sample_driver_available: Driver,
    sample_order_validated: Order,  # CHANGEMENT: Utiliser validated pour simuler un échec
):
    """Tests that a ValueError is raised if an order is not in 'pending' status (Service logic)."""
    mock_user_dao.find_user_by_id.return_value = sample_driver_available
    mock_order_dao.find_order_by_id.return_value = sample_order_validated
    with pytest.raises(
        ValueError, match="has not the pending status. Current status: validated"
    ):  # CHANGEMENT: Message exact
        service.create_and_assign_delivery(order_ids=[sample_order_validated.id], user_id=sample_driver_available.id)


def test_create_delivery_dao_failure(
    service: DriverService,
    mock_user_dao: MagicMock,
    mock_order_dao: MagicMock,
    mock_delivery_dao: MagicMock,
    sample_driver_available: Driver,
    sample_order_pending: Order,
):
    """Tests that an Exception is raised if the DAO fails to add the delivery."""
    mock_user_dao.find_user_by_id.return_value = sample_driver_available
    mock_order_dao.find_order_by_id.return_value = sample_order_pending
    mock_delivery_dao.add_delivery.return_value = None  # Simulate DAO failure

    with pytest.raises(Exception, match="Failed to create and assign the delivery in the database."):
        service.create_and_assign_delivery(order_ids=[101], user_id=1)


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
    with pytest.raises(ValueError, match="No delivery found with ID 999."):
        service.complete_delivery(999)


def test_complete_delivery_validation_wrong_status(
    service: DriverService, mock_delivery_dao: MagicMock, sample_delivery_pending: Delivery
):
    """Tests that a ValueError is raised if the delivery is not 'in_progress'."""
    mock_delivery_dao.find_delivery_by_id.return_value = sample_delivery_pending
    with pytest.raises(ValueError, match="Only 'in_progress' deliveries can be completed. Current status: pending"):
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
    # Utiliser side_effect pour que le MockOrderDAO lève une exception lors de l'appel à update_order
    mock_order_dao.update_order.side_effect = Exception("DB Error")

    # Act
    service.complete_delivery(sample_delivery_inprogress.id)

    # Assert
    # Check that the log was written
    # Note: caplog.text capture la sortie de logging.warning
    assert (
        "Could not update status for orders in delivery 50: DB Error" in caplog.text
    )  # CHANGEMENT: Assurer que l'ID est dans le log

    # Check that the delivery *was* still updated and completed
    assert sample_delivery_inprogress.status == "completed"
    mock_delivery_dao.update_delivery.assert_called_once_with(sample_delivery_inprogress)


def test_complete_delivery_dao_failure(
    service: DriverService, mock_delivery_dao: MagicMock, sample_delivery_inprogress: Delivery
):
    """Tests that an Exception is raised if the delivery update fails."""
    mock_delivery_dao.find_delivery_by_id.return_value = sample_delivery_inprogress
    mock_delivery_dao.update_delivery.return_value = None  # Simulate DAO failure

    with pytest.raises(Exception, match="Failed to update delivery status to completed."):
        service.complete_delivery(sample_delivery_inprogress.id)


# --- Test Get Delivery Details (Behavior changed in Service) ---


def test_get_delivery_details_returns_dicts(
    service: DriverService,
    mock_delivery_dao: MagicMock,
    mock_user_dao: MagicMock,
    sample_delivery_inprogress: Delivery,
    sample_address: Address,
    sample_customer: Customer,
):
    """
    Tests that the updated get_delivery_details returns a tuple of two dictionaries (addresses, customers).
    """
    # Arrange
    mock_delivery_dao.find_delivery_by_id.return_value = sample_delivery_inprogress
    # Mock find_user_by_id: Le service utilise order.customer.name pour trouver l'utilisateur, ce qui est probablement un bug
    # On simule que find_user_by_id(name) retourne l'objet Customer
    mock_user_dao.find_user_by_id.return_value = sample_customer

    # Act
    result_addresses, result_customers = service.get_delivery_details(sample_delivery_inprogress.id)

    # Assert
    mock_delivery_dao.find_delivery_by_id.assert_called_once_with(sample_delivery_inprogress.id)

    # Vérification des adresses
    expected_address = sample_address
    assert isinstance(result_addresses, dict)
    assert len(result_addresses) == 1
    assert result_addresses[sample_delivery_inprogress.orders[0].id] == expected_address

    # Vérification des clients
    expected_customer = sample_customer
    assert isinstance(result_customers, dict)
    assert len(result_customers) == 1
    assert result_customers[sample_delivery_inprogress.orders[0].id] == expected_customer


def test_get_delivery_details_not_found(service: DriverService, mock_delivery_dao: MagicMock):
    """Tests that a ValueError is raised if the delivery is not found."""
    mock_delivery_dao.find_delivery_by_id.return_value = None

    with pytest.raises(ValueError, match="No delivery found with ID 999."):
        service.get_delivery_details(999)


# --- Test List Pending Orders (Renamed from list_pending_deliveries) ---


def test_list_pending_orders_success(
    service: DriverService,
    mock_order_dao: MagicMock,
    sample_order_pending: Order,
    sample_order_validated: Order,
):
    """Tests that only orders with 'pending' status are returned."""
    all_orders = [sample_order_pending, sample_order_validated]
    mock_order_dao.find_all_orders.return_value = all_orders

    result = service.list_pending_orders()

    assert result == [sample_order_pending]
    mock_order_dao.find_all_orders.assert_called_once()


def test_list_pending_orders_empty(service: DriverService, mock_order_dao: MagicMock):
    """Tests that an empty list is returned if no orders exist."""
    mock_order_dao.find_all_orders.return_value = []

    result = service.list_pending_orders()

    assert result == []


# --- Nouveaux tests pour get_assigned_delivery et get_itinerary ---


def test_get_assigned_delivery_success(
    service: DriverService, mock_delivery_dao: MagicMock, sample_delivery_inprogress: Delivery
):
    """Tests retrieving the assigned delivery for a driver."""
    mock_delivery_dao.find_in_progress_deliveries_by_driver.return_value = [sample_delivery_inprogress]

    result = service.get_assigned_delivery(user_id=1)

    mock_delivery_dao.find_in_progress_deliveries_by_driver.assert_called_once_with(1)
    assert result == [sample_delivery_inprogress]


def test_get_assigned_delivery_no_delivery(service: DriverService, mock_delivery_dao: MagicMock):
    """Tests retrieving no assigned delivery for a driver."""
    mock_delivery_dao.find_in_progress_deliveries_by_driver.return_value = []

    result = service.get_assigned_delivery(user_id=1)

    assert result == []


def test_get_itinerary_success(
    service: DriverService,
    mock_delivery_dao: MagicMock,
    mock_user_dao: MagicMock,
    sample_driver_available: Driver,
    sample_delivery_inprogress: Delivery,
    mocker,
):
    """Tests retrieving the itinerary for an ongoing delivery."""
    # Arrange
    mock_delivery_dao.find_in_progress_deliveries_by_driver.return_value = [sample_delivery_inprogress]
    mock_user_dao.find_user_by_id.return_value = sample_driver_available

    # 1. Stocker la référence à l'objet mock créé par le patch
    expected_itinerary = "Itinerary map URL"
    mock_itinerary_func = mocker.patch(
        "src.Service.driver_service.ApiMapsService.Driveritinerary", return_value=expected_itinerary
    )  # <-- Capture de l'objet Mock

    # Act
    result = service.get_itinerary(user_id=sample_driver_available.id)

    # Assert
    expected_addresses = [
        f"{sample_delivery_inprogress.orders[0].address.street_number} "
        f"{sample_delivery_inprogress.orders[0].address.street_name}, "
        f"{sample_delivery_inprogress.orders[0].address.city}, France"
    ]

    # 2. Utiliser l'objet mock stocké pour l'assertion
    mock_itinerary_func.assert_called_once_with(expected_addresses)
    assert result == expected_itinerary


def test_get_itinerary_no_delivery(service: DriverService, mock_delivery_dao: MagicMock):
    """Tests get_itinerary when no delivery is in progress."""
    mock_delivery_dao.find_in_progress_deliveries_by_driver.return_value = []

    result = service.get_itinerary(user_id=1)

    assert result is None


def test_get_itinerary_driver_not_found(service: DriverService, mock_delivery_dao: MagicMock, mock_user_dao: MagicMock):
    """Tests get_itinerary when the driver ID is invalid."""
    mock_delivery_dao.find_in_progress_deliveries_by_driver.return_value = [MagicMock(spec=Delivery)]
    mock_user_dao.find_user_by_id.return_value = None

    with pytest.raises(ValueError, match="No valid driver found with ID 99"):
        service.get_itinerary(user_id=99)
