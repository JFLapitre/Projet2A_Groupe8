from unittest import mock
from unittest.mock import ANY, MagicMock

import pytest

from src.DAO.DBConnector import DBConnector
from src.DAO.userDAO import UserDAO
from src.Model.customer import Customer
from src.Service.authentication_service import AuthenticationService
from src.Service.password_service import PasswordService


@pytest.fixture
def mock_db_connector() -> MagicMock:
    """
    Provides a mock for the DBConnector.
    """
    return MagicMock(spec=DBConnector)


@pytest.fixture
def mock_password_service() -> MagicMock:
    """
    Provides a mock for the PasswordService.
    """
    mock_ps = MagicMock(spec=PasswordService)

    mock_ps.check_password_strength.return_value = None
    mock_ps.create_salt.return_value = "generated_mock_salt"
    mock_ps.hash_password.return_value = "generated_mock_hash"
    return mock_ps


@pytest.fixture
def mock_user_dao(request) -> mock.MagicMock:
    """
    Simule (patch) la classe UserDAO sans utiliser la fixture 'mocker'.
    """
    mock_instance = mock.MagicMock()
    mock_instance.find_user_by_username.return_value = None
    patcher = mock.patch("src.Service.authentication_service.UserDAO", return_value=mock_instance)
    patcher.start()
    request.addfinalizer(patcher.stop)

    return mock_instance


@pytest.fixture
def dummy_customer() -> Customer:
    """
    Provides a constant Customer object for login tests.
    The "real" password for this user is "correct_password".
    """
    return Customer(
        id_user=1,
        username="existing_user",
        phone_number="1234567890",
        salt="jambon",
        hash_password="7877d4860ef88458096f549b618667d860540db5d59b1d153557d5cdbe1221e7",
    )


@pytest.fixture
def service(
    mock_db_connector: MagicMock, mock_password_service: MagicMock, mock_user_dao: MagicMock
) -> AuthenticationService:
    """
    Provides an AuthenticationService instance for each test,
    injected with the necessary mocks.
    """
    # Note: mock_user_dao has already patched the UserDAO class,
    # so the AuthenticationService constructor will use the mock.
    return AuthenticationService(db_connector=mock_db_connector, password_service=mock_password_service)


# --- Tests for login() method ---


def test_login_successful(
    service: AuthenticationService, mock_user_dao: MagicMock, mock_password_service: MagicMock, dummy_customer: Customer
):
    """
    Tests that a user can successfully log in with a valid username and password.
    """
    username = "existing_user"
    password = "soleil1234"

    mock_user_dao.find_user_by_username.return_value = dummy_customer
    mock_password_service.hash_password.return_value = (
        "7877d4860ef88458096f549b618667d860540db5d59b1d153557d5cdbe1221e7"
    )

    try:
        logged_in_user = service.login(username, password)

        assert logged_in_user is dummy_customer
        mock_user_dao.find_user_by_username.assert_called_with(username)
        mock_password_service.hash_password.assert_called_with(password, "jambon")

    except Exception as e:
        pytest.fail(f"login raised an unexpected exception: {e}")


def test_login_user_not_found(service: AuthenticationService, mock_user_dao: MagicMock):
    """
    Tests that login raises a ValueError if the user does not exist.
    """

    with pytest.raises(ValueError) as e:
        service.login("unknown_user", "any_password")

    assert "User not found" in str(e.value)
    mock_user_dao.find_user_by_username.assert_called_with("unknown_user")


def test_login_incorrect_password(
    service: AuthenticationService, mock_user_dao: MagicMock, mock_password_service: MagicMock, dummy_customer: Customer
):
    """
    Tests that login raises a ValueError if the password is incorrect.
    """
    username = "existing_user"
    wrong_password = "wrong_password"
    mock_user_dao.find_user_by_username.return_value = dummy_customer
    mock_password_service.hash_password.return_value = "different_hash_value"

    with pytest.raises(ValueError) as e:
        service.login(username, wrong_password)

    assert "Incorrect password" in str(e.value)
    mock_password_service.hash_password.assert_called_with(wrong_password, "existing_salt")


# --- Tests for register() method ---


def test_register_successful(
    service: AuthenticationService, mock_user_dao: MagicMock, mock_password_service: MagicMock
):
    """
    Tests the successful registration of a new user.
    """
    username = "new_user"
    password = "ValidPassword123"
    phone = "555-0123"

    # Configure mocks for this flow
    expected_salt = "generated_mock_salt"
    expected_hash = "hashed_ValidPassword123_with_salt"
    mock_password_service.create_salt.return_value = expected_salt
    mock_password_service.hash_password.return_value = expected_hash

    try:
        new_user = service.register(username, password, phone)

        # Verify the complete call chain
        mock_user_dao.find_user_by_username.assert_called_with(username)
        mock_password_service.check_password_strength.assert_called_with(password)
        mock_password_service.create_salt.assert_called_once()
        mock_password_service.hash_password.assert_called_with(password, expected_salt)

        # Verify that add_user was called with the correct Customer object
        # ANY is used because it is a new Customer instance
        mock_user_dao.add_user.assert_called_once_with(ANY)

        # More detailed inspection of the object passed to add_user
        created_user_arg = mock_user_dao.add_user.call_args[0][0]
        assert isinstance(created_user_arg, Customer)
        assert created_user_arg.username == username
        assert created_user_arg.password == expected_hash  # Must store the HASH
        assert created_user_arg.salt == expected_salt
        assert created_user_arg.phone_number == phone

        # Verify that the returned user is the one that was created
        assert new_user is created_user_arg

    except Exception as e:
        pytest.fail(f"register raised an unexpected exception: {e}")


def test_register_username_exists(service: AuthenticationService, mock_user_dao: MagicMock, dummy_customer: Customer):
    """
    Tests that register raises a ValueError if the username is already taken.
    """
    # Configure mock: find_user returns an existing user
    mock_user_dao.find_user_by_username.return_value = dummy_customer

    existing_username = "existing_user"  # The same as dummy_customer

    with pytest.raises(ValueError) as e:
        service.register(existing_username, "any_password", "any_phone")

    assert f"Username '{existing_username}' already exists" in str(e.value)
    mock_user_dao.find_user_by_username.assert_called_with(existing_username)


def test_register_weak_password(
    service: AuthenticationService, mock_user_dao: MagicMock, mock_password_service: MagicMock
):
    """
    Tests that register raises an Exception if the
    password strength check fails.
    """
    weak_password = "short"
    error_message = "Password length must be at least 8 characters"

    # Configure mocks
    # mock_user_dao.find_user_by_username returns None (default)
    # Configure check_password_strength to raise the exception
    mock_password_service.check_password_strength.side_effect = Exception(error_message)

    with pytest.raises(Exception) as e:
        service.register("another_user", weak_password, "any_phone")

    assert error_message in str(e.value)

    # Verify that the process stopped before creating salt/hash/user
    mock_user_dao.find_user_by_username.assert_called_with("another_user")
    mock_password_service.check_password_strength.assert_called_with(weak_password)
    mock_password_service.create_salt.assert_not_called()
    mock_password_service.hash_password.assert_not_called()
    mock_user_dao.add_user.assert_not_called()
