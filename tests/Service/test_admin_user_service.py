from unittest.mock import ANY, MagicMock

import pytest

# Import all models, DAOs, and the service to be tested
from src.DAO.DBConnector import DBConnector
from src.DAO.userDAO import UserDAO
from src.Model.admin import Admin
from src.Model.customer import Customer
from src.Model.driver import Driver

# Import the service to test
from src.Service.admin_user_service import AdminUserService
from src.Service.password_service import PasswordService

# --- Fixtures ---


@pytest.fixture
def mock_db_connector():
    """Provides a mock DBConnector."""
    return MagicMock(spec=DBConnector)


@pytest.fixture
def mock_user_dao():
    """Provides a mock UserDAO."""
    return MagicMock(spec=UserDAO)


@pytest.fixture
def mock_password_service():
    """Provides a mock PasswordService instance."""
    mock_ps = MagicMock(spec=PasswordService)
    # Configure les valeurs par défaut pour les appels de hachage réussis
    mock_ps.create_salt.return_value = "generated_salt"
    mock_ps.hash_password.return_value = "generated_hash"
    mock_ps.check_password_strength.return_value = None
    return mock_ps


@pytest.fixture
def service(mock_db_connector, mock_user_dao, mock_password_service, mocker):
    """
    Provides an AdminUserService instance with mocked UserDAO and PasswordService.
    """
    # Patch the *constructors* for UserDAO and PasswordService to return our mocks
    mocker.patch("src.Service.admin_user_service.UserDAO", return_value=mock_user_dao)

    # Create the service. Its __init__ will use the mocks.
    # Note: L'argument 'password_service' est nécessaire car il n'est plus une classe par défaut
    admin_service = AdminUserService(db_connector=mock_db_connector, password_service=mock_password_service)

    assert admin_service.user_dao == mock_user_dao
    assert admin_service.password_service == mock_password_service

    return admin_service


# --- Data Fixtures ---


@pytest.fixture
def sample_admin():
    """Provides a mock Admin user."""
    return MagicMock(spec=Admin, id=1, name="Sample Admin")


@pytest.fixture
def sample_driver():
    """Provides a mock Driver user."""
    return MagicMock(spec=Driver, id=2, name="Sample Driver", availability=True)


@pytest.fixture
def sample_customer():
    """Provides a mock Customer user."""
    return MagicMock(spec=Customer, id=3, name="Sample Customer")


@pytest.fixture
def sample_user_list(sample_admin, sample_driver, sample_customer):
    """Provides a list of various users."""
    return [sample_admin, sample_driver, sample_customer]


@pytest.fixture
def sample_driver_list(sample_driver):
    """Provides a list containing only drivers."""
    driver2 = MagicMock(spec=Driver, id=4, name="Driver Two", availability=False)
    return [sample_driver, driver2]


# --- Test Create Admin Account ---


def test_create_admin_account_success(
    service: AdminUserService, mock_user_dao: MagicMock, mock_password_service: MagicMock
):
    """Tests the successful creation of an admin account."""
    # Arrange
    mock_user_dao.find_user_by_username.return_value = None  # Username is available
    mock_password_service.create_salt.return_value = "testsalt"
    mock_password_service.hash_password.return_value = "testhash123"

    # Simulate the DAO returning the created admin
    created_admin_mock = MagicMock(spec=Admin, id=1, username="newadmin", name="New Admin")
    mock_user_dao.add_user.return_value = created_admin_mock

    # Act
    result = service.create_admin_account("newadmin", "ValidPass123", "New Admin", "123456")

    # Assert
    mock_user_dao.find_user_by_username.assert_called_once_with("newadmin")
    mock_password_service.check_password_strength.assert_called_once_with("ValidPass123")
    mock_password_service.create_salt.assert_called_once()
    mock_password_service.hash_password.assert_called_once_with("ValidPass123", "testsalt")

    # Check that the DAO was called with a correctly formed Admin object
    mock_user_dao.add_user.assert_called_once_with(ANY)
    called_admin_obj = mock_user_dao.add_user.call_args[0][0]

    assert isinstance(called_admin_obj, Admin)
    assert called_admin_obj.username == "newadmin"
    assert called_admin_obj.hash_password == "testhash123"
    assert called_admin_obj.salt == "testsalt"
    assert called_admin_obj.phone_number == "123456"

    assert result == created_admin_mock


def test_create_admin_account_username_exists(
    service: AdminUserService, mock_user_dao: MagicMock, mock_password_service: MagicMock
):
    """Tests that a ValueError is raised if the username already exists."""
    # Arrange
    mock_user_dao.find_user_by_username.return_value = MagicMock(spec=Admin)  # Username found

    # Act / Assert
    with pytest.raises(ValueError, match="Username 'admin' already exists."):
        service.create_admin_account("admin", "pass123", "Name", "111")

    # Check that no password hashing or user creation was attempted
    mock_password_service.hash_password.assert_not_called()
    mock_user_dao.add_user.assert_not_called()


@pytest.mark.parametrize(
    "username, password, name",
    [
        ("", "pass123", "Name"),
        ("admin", "", "Name"),
        ("admin", "pass123", ""),
    ],
)
def test_create_admin_account_empty_fields(service: AdminUserService, username, password, name):
    """Tests that required fields (username, password, name) cannot be empty."""
    with pytest.raises(ValueError, match="Username, password, and name are required."):
        service.create_admin_account(username, password, name, "123456")


def test_create_admin_account_weak_password(
    service: AdminUserService, mock_user_dao: MagicMock, mock_password_service: MagicMock
):
    """Tests that a weak password (as defined by PasswordService) raises an exception."""
    # Arrange
    mock_user_dao.find_user_by_username.return_value = None
    # Simulate PasswordService raising an error
    mock_password_service.check_password_strength.side_effect = ValueError("Password is too weak.")

    # Act / Assert
    with pytest.raises(ValueError, match="Password is too weak."):
        service.create_admin_account("newadmin", "123", "New Admin", "123456")

    # Check that user creation was not attempted
    mock_user_dao.add_user.assert_not_called()


def test_create_admin_account_dao_failure(
    service: AdminUserService, mock_user_dao: MagicMock, mock_password_service: MagicMock
):
    """Tests that an Exception is raised if the DAO fails to add the user."""
    # Arrange
    mock_user_dao.find_user_by_username.return_value = None
    mock_password_service.create_salt.return_value = "testsalt"
    mock_password_service.hash_password.return_value = "testhash123"
    mock_user_dao.add_user.return_value = None  # Simulate DAO failure

    # Act / Assert
    with pytest.raises(Exception, match="Failed to create admin account in the database."):
        service.create_admin_account("newadmin", "ValidPass123", "New Admin", "123456")


# --- Test Create Driver Account ---


def test_create_driver_account_success_secure(
    service: AdminUserService, mock_user_dao: MagicMock, mock_password_service: MagicMock
):
    """
    Tests successful creation of a driver, verifying that hashing and salting are used.
    """
    # Arrange
    mock_user_dao.find_user_by_username.return_value = None  # Username is available
    mock_password_service.create_salt.return_value = "driversalt"
    mock_password_service.hash_password.return_value = "driverhash"

    created_driver_mock = MagicMock(spec=Driver, id=2, username="newdriver", name="New Driver", availability=True)
    mock_user_dao.add_user.return_value = created_driver_mock

    # Act
    result = service.create_driver_account(
        "newdriver", "DriverPass123", "New Driver", "555666", "car", availability=True
    )

    # Assert
    mock_user_dao.find_user_by_username.assert_called_once_with("newdriver")

    # Verify PasswordService calls (now fully implemented in the service)
    mock_password_service.check_password_strength.assert_called_once_with("DriverPass123")
    mock_password_service.create_salt.assert_called_once()
    mock_password_service.hash_password.assert_called_once_with("DriverPass123", "driversalt")

    # Check that the DAO was called with a Driver object containing hash/salt
    mock_user_dao.add_user.assert_called_once_with(ANY)
    called_driver_obj = mock_user_dao.add_user.call_args[0][0]

    assert isinstance(called_driver_obj, Driver)
    assert called_driver_obj.username == "newdriver"
    assert called_driver_obj.hash_password == "driverhash"  # Should be the hashed value
    assert called_driver_obj.salt == "driversalt"
    assert called_driver_obj.vehicle_type == "car"
    assert called_driver_obj.availability is True

    assert result == created_driver_mock


def test_create_driver_account_username_exists(service: AdminUserService, mock_user_dao: MagicMock):
    """Tests that a ValueError is raised if the driver's username already exists."""
    # Arrange
    mock_user_dao.find_user_by_username.return_value = MagicMock(spec=Customer)  # Username found

    # Act / Assert
    with pytest.raises(ValueError, match="Username 'driver' already exists."):
        service.create_driver_account("driver", "pass123", "Name", "111", "van")

    mock_user_dao.add_user.assert_not_called()


@pytest.mark.parametrize(
    "username, password, name, phone_number, vehicle_type, error_match",
    [
        ("", "p", "N", "1", "car", "Username, password, name, and phone number are required."),
        ("u", "", "N", "1", "car", "Username, password, name, and phone number are required."),
        ("u", "p", "", "1", "car", "Username, password, name, and phone number are required."),
        ("u", "p", "N", "", "car", "Username, password, name, and phone number are required."),
        ("u", "p", "N", "1", "", "Vehicle type is required for a driver."),
    ],
)
def test_create_driver_account_empty_required_fields(
    service: AdminUserService, username, password, name, phone_number, vehicle_type, error_match
):
    """Tests that required fields cannot be empty."""
    with pytest.raises(ValueError, match=error_match):
        service.create_driver_account(username, password, name, phone_number, vehicle_type)

    service.user_dao.find_user_by_username.assert_not_called()


def test_create_driver_account_weak_password(
    service: AdminUserService, mock_user_dao: MagicMock, mock_password_service: MagicMock
):
    """Tests that a weak password (as defined by PasswordService) raises an exception."""
    # Arrange
    mock_user_dao.find_user_by_username.return_value = None
    # Simulate PasswordService raising an error
    mock_password_service.check_password_strength.side_effect = ValueError("Driver password is too weak.")

    # Act / Assert
    with pytest.raises(ValueError, match="Driver password is too weak."):
        service.create_driver_account("newdriver", "123", "New Driver", "555666", "car")

    # Check that user creation was not attempted
    mock_user_dao.add_user.assert_not_called()


def test_create_driver_account_dao_failure(service: AdminUserService, mock_user_dao: MagicMock):
    """Tests that an Exception is raised if the DAO fails to add the driver."""
    # Arrange
    mock_user_dao.find_user_by_username.return_value = None
    mock_user_dao.add_user.return_value = None  # Simulate DAO failure

    # Act / Assert
    with pytest.raises(Exception, match="Failed to create driver account in the database."):
        service.create_driver_account("newdriver", "DriverPass123", "New Driver", "555666", "car")


# --- Test Update Driver Availability ---


def test_update_driver_availability_success(service: AdminUserService, mock_user_dao: MagicMock, sample_driver: Driver):
    """Tests successfully updating a driver's availability from True to False."""
    # Arrange
    sample_driver.availability = True  # Initial state
    mock_user_dao.find_user_by_id.return_value = sample_driver
    mock_user_dao.update_user.return_value = sample_driver

    # Act
    result = service.update_driver_availability(driver_id=2, availability=False)

    # Assert
    mock_user_dao.find_user_by_id.assert_called_once_with(2)
    assert sample_driver.availability is False  # Check the object was modified
    mock_user_dao.update_user.assert_called_once_with(sample_driver)
    assert result == sample_driver


def test_update_driver_availability_no_change(
    service: AdminUserService, mock_user_dao: MagicMock, sample_driver: Driver
):
    """Tests that updating to the same status still works."""
    # Arrange
    sample_driver.availability = True  # Initial state
    mock_user_dao.find_user_by_id.return_value = sample_driver
    mock_user_dao.update_user.return_value = sample_driver

    # Act
    result = service.update_driver_availability(driver_id=2, availability=True)

    # Assert
    assert sample_driver.availability is True
    mock_user_dao.update_user.assert_called_once_with(sample_driver)
    assert result == sample_driver


def test_update_driver_availability_not_found(service: AdminUserService, mock_user_dao: MagicMock):
    """Tests that a ValueError is raised if the driver ID is not found."""
    # Arrange
    mock_user_dao.find_user_by_id.return_value = None

    # Act / Assert
    with pytest.raises(ValueError, match="No valid driver found with ID 999"):
        service.update_driver_availability(driver_id=999, availability=True)

    mock_user_dao.update_user.assert_not_called()


def test_update_driver_availability_user_is_customer(
    service: AdminUserService, mock_user_dao: MagicMock, sample_customer: Customer
):
    """Tests that a ValueError is raised if the user ID is not a Driver."""
    # Arrange
    mock_user_dao.find_user_by_id.return_value = sample_customer

    # Act / Assert
    with pytest.raises(ValueError, match="No valid driver found with ID 3"):
        service.update_driver_availability(driver_id=3, availability=True)

    mock_user_dao.update_user.assert_not_called()


def test_update_driver_availability_dao_failure(
    service: AdminUserService, mock_user_dao: MagicMock, sample_driver: Driver
):
    """Tests that an Exception is raised if the DAO update fails."""
    # Arrange
    mock_user_dao.find_user_by_id.return_value = sample_driver
    mock_user_dao.update_user.return_value = None  # Simulate DAO failure

    # Act / Assert
    with pytest.raises(Exception, match="Failed to update driver availability."):
        service.update_driver_availability(driver_id=2, availability=False)


# --- Test Delete User ---


def test_delete_user_success(service: AdminUserService, mock_user_dao: MagicMock, sample_driver: Driver):
    """Tests that any user (e.g., a Driver) can be deleted."""
    # Arrange
    mock_user_dao.find_user_by_id.return_value = sample_driver
    mock_user_dao.delete_user.return_value = True  # Simulate successful deletion

    # Act
    result = service.delete_user(user_id=2)

    # Assert
    mock_user_dao.find_user_by_id.assert_called_once_with(2)
    mock_user_dao.delete_user.assert_called_once_with(2)
    assert result is True


def test_delete_user_not_found(service: AdminUserService, mock_user_dao: MagicMock):
    """Tests that a ValueError is raised if the user to delete is not found."""
    # Arrange
    mock_user_dao.find_user_by_id.return_value = None

    # Act / Assert
    with pytest.raises(ValueError, match="No user found with ID 999."):
        service.delete_user(user_id=999)

    mock_user_dao.delete_user.assert_not_called()


def test_delete_user_dao_failure(service: AdminUserService, mock_user_dao: MagicMock, sample_admin: Admin):
    """Tests that an Exception is raised if the DAO deletion fails."""
    # Arrange
    mock_user_dao.find_user_by_id.return_value = sample_admin
    mock_user_dao.delete_user.return_value = False  # Simulate DAO failure

    # Act / Assert
    with pytest.raises(Exception, match="Failed to delete user 1."):
        service.delete_user(user_id=1)


# --- Test List All Users ---


def test_list_all_users_success(service: AdminUserService, mock_user_dao: MagicMock, sample_user_list: list):
    """Tests retrieving a list of all user types."""
    # Arrange
    mock_user_dao.find_all.return_value = sample_user_list

    # Act
    result = service.list_all_users()

    # Assert
    mock_user_dao.find_all.assert_called_once_with()  # Called with no args
    assert result == sample_user_list
    assert len(result) == 3


def test_list_all_users_empty(service: AdminUserService, mock_user_dao: MagicMock):
    """Tests retrieving an empty list when no users exist."""
    # Arrange
    mock_user_dao.find_all.return_value = []

    # Act
    result = service.list_all_users()

    # Assert
    assert result == []


# --- Test List Drivers ---


def test_list_drivers_success(service: AdminUserService, mock_user_dao: MagicMock, sample_driver_list: list):
    """Tests retrieving a list of only 'driver' type users."""
    # Arrange
    mock_user_dao.find_all.return_value = sample_driver_list

    # Act
    result = service.list_drivers()

    # Assert
    # Check that 'find_all' was called with the correct filter
    mock_user_dao.find_all.assert_called_once_with(user_type="driver")
    assert result == sample_driver_list
    assert len(result) == 2


def test_list_drivers_empty(service: AdminUserService, mock_user_dao: MagicMock):
    """Tests retrieving an empty list when no drivers exist."""
    # Arrange
    mock_user_dao.find_all.return_value = []

    # Act
    result = service.list_drivers()

    # Assert
    mock_user_dao.find_all.assert_called_once_with(user_type="driver")
    assert result == []
