from unittest.mock import ANY, MagicMock, patch
import os
import pytest

from src.DAO.addressDAO import AddressDAO
from src.DAO.bundleDAO import BundleDAO
from src.DAO.DBConnector import DBConnector
from src.DAO.deliveryDAO import DeliveryDAO
from src.DAO.itemDAO import ItemDAO
from src.DAO.orderDAO import OrderDAO
from src.DAO.userDAO import UserDAO
from src.Model.delivery import Delivery

from src.Service.api_maps_service import ApiMapsService

# --- Fixtures ---


@pytest.fixture
def mock_db_connector():
    """Provides a mock DBConnector."""
    return MagicMock(spec=DBConnector)


@pytest.fixture
def mock_order_dao():
    """Provides a mock OrderDAO."""
    return MagicMock(spec=OrderDAO)


@pytest.fixture
def mock_user_dao():
    """Provides a mock UserDAO."""
    return MagicMock(spec=UserDAO)


@pytest.fixture
def mock_item_dao():
    """Provides a mock ItemDAO."""
    return MagicMock(spec=ItemDAO)

@pytest.fixture
def mock_address_dao():
    """Provides a mock AddressDAO."""
    return MagicMock(spec=AddressDAO)

@pytest.fixture
def mock_delivery_dao():
    """Provides a mock DeliveryDAO."""
    return MagicMock(spec=DeliveryDAO)


@pytest.fixture
def mock_bundle_dao():
    """Provides a mock BundleDAO."""
    return MagicMock(spec=BundleDAO)


def test_api_key_exists_in_real_env():
    """Vérifie réellement que la clé GOOGLE_MAPS_API_KEY est chargée depuis l'environnement."""

    service = ApiMapsService()

    # The API Key needs to exist in the env 
    assert service.api_key is not None, "GOOGLE_MAPS_API_KEY n'est pas définie dans le .env ou l'environnement"
    assert service.api_key != "", "GOOGLE_MAPS_API_KEY est vide dans l'environnement"

    print("Clé trouvée :", service.api_key)


    print("Clé trouvée :", service.api_key)


def test_itinerary_created(service: ApiMapsService, mock_delievry_dao: MagicMock, sample_delivery: Delivery):
    """Tests successful creation of a itinerary."""
    mock_delivery_dao.find_delivery_by_id.return_value = sample_delivery
    mock_item_dao.delete_item.return_value = True

    service.DriverItenerary(1)

    mock_item_dao.find_item_by_id.assert_called_once_with(1)
    mock_item_dao.delete_item.assert_called_once_with(1)