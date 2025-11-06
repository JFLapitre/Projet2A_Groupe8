import pytest
from typing import Optional, Union, Literal, Dict, Any, List
from datetime import date
from src.DAO.addressDAO import AddressDAO
from src.Model.address import Address


class MockDBConnector:
    def __init__(self):
        self.address = [
            {
                "id_address": 1,
                "city": 'Lyon',
                "postal_code": 69000,
                "street_name": 'Rue de la République',
                "street_number": "1"
            },
            {
                "id_address": 2,
                "city": 'Auxerre',
                "postal_code": 89000,
                "street_name": 'Rue des Boussicats',
                "street_number": "3 bis"
            }
        ]
        self.next_address_id = 3

    def sql_query(self,
                  query: str,
                  data: Optional[Union[tuple, list, dict]] = None,
                  return_type: Optional[Union[Literal["one"], Literal["all"], None]] = "one"
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], bool, None]:

        q = " ".join(query.lower().split())

        # find_address_by_id
        if "select * from address where id_address" in q and return_type == "one":
            if isinstance(data, dict) and 'id_address' in data:
                address_id = data.get("id_address")
                for address in self.address:
                    if address["id_address"] == address_id:
                        return address.copy()

            return None

        # find_all_addresses
        if "select * from address" in q and return_type == "all":
            return [addr.copy() for addr in self.address]

        # add_address
        if "insert into address" in q and "returning" in q and return_type == "one":
            if not isinstance(data, dict):
                return False

            new_id = self.next_address_id
            self.next_address_id += 1

            created_address = {
                "id_address": new_id,
                "city": data["city"],
                "postal_code": data["postal_code"],
                "street_name": data["street_name"],
                "street_number": data["street_number"]
            }

            self.address.append(created_address)
            return created_address

        # update_address
        if "update address" in q and "where id_address" in q and return_type == "one":
            if not isinstance(data, dict) or 'id_address' not in data:
                return False
            address_id_to_update = data.get("id_address")
            for address in self.address:
                if address["id_address"] == address_id_to_update:
                    address["city"] = data.get("city", address["city"])
                    address["postal_code"] = data.get("postal_code", address["postal_code"])
                    address["street_name"] = data.get("street_name", address["street_name"])
                    address["street_number"] = data.get("street_number", address["street_number"])
                    return {"id_address": address_id_to_update}
            return None

        # delete_address
        if "delete from address" in q and "where id_address" in q and return_type == "one":
            if isinstance(data, dict) and 'id_address' in data:
                address_id_to_delete = data.get("id_address")
                initial_len = len(self.address)
                self.address = [addr for addr in self.address if addr["id_address"] != address_id_to_delete]
                if len(self.address) < initial_len:
                    return {"id_address": address_id_to_delete}
                else:
                    return None

            return None

        if "simulate_db_error" in q:
            raise Exception("Simulated Database Error")

        return None


@pytest.fixture
def mock_db_connector():
    return MockDBConnector()

@pytest.fixture
def address_dao(mock_db_connector) -> AddressDAO:
    return AddressDAO(db_connector=mock_db_connector)

def test_find_address_by_id_existing(address_dao: AddressDAO):
    """Teste la récupération d'une adresse existante par ID (ID 1 est mocké)."""
    found_address = address_dao.find_address_by_id(1)

    assert found_address is not None
    assert isinstance(found_address, Address)
    assert found_address.id_address == 1
    assert found_address.city == 'Lyon'

def test_find_address_by_id_non_existing(address_dao: AddressDAO):
    """Teste la récupération d'une adresse inexistante."""
    found_address = address_dao.find_address_by_id(999)

    assert found_address is None


def test_find_all_addresses(address_dao: AddressDAO):
    """Teste la récupération de toutes les adresses mockées."""
    all_addresses = address_dao.find_all_addresses()

    assert isinstance(all_addresses, list)
    assert len(all_addresses) == 2
    assert all(isinstance(a, Address) for a in all_addresses)
    assert all_addresses[0].id_address == 1


def test_add_address_success(address_dao: AddressDAO, mock_db_connector):
    """Teste l'ajout d'une nouvelle adresse et vérifie qu'elle a un ID."""
    new_address = Address(
        city="Paris",
        postal_code=75001,
        street_name="Rue de Rivoli",
        street_number="10"
    )
    initial_count = len(mock_db_connector.address)

    created_address = address_dao.add_address(new_address)

    assert created_address is not None
    assert created_address.id_address == mock_db_connector.next_address_id - 1
    assert created_address.city == "Paris"
    assert len(mock_db_connector.address) == initial_count + 1


def test_update_address_success(address_dao: AddressDAO, mock_db_connector):
    """Teste la mise à jour réussie d'une adresse existante."""
    address_to_update = Address(
        id_address=1,
        city='Lyon',
        postal_code=69001,
        street_name='Rue de la République',
        street_number="1"
    )

    result = address_dao.update_address(address_to_update)

    assert result is True
    updated_mock_address = next(addr for addr in mock_db_connector.address if addr["id_address"] == 1)
    assert updated_mock_address["postal_code"] == 69001

def test_update_address_non_existing(address_dao: AddressDAO):
    """Teste la mise à jour d'une adresse qui n'existe pas."""
    non_existing_address = Address(
        id_address=999,
        city='Nowhere',
        postal_code=11111,
        street_name='Ghost Street',
        street_number="0"
    )

    result = address_dao.update_address(non_existing_address)

    assert result is False


def test_delete_address_success(address_dao: AddressDAO, mock_db_connector):
    """Teste la suppression réussie d'une adresse existante (ID 2)."""
    id_to_delete = 2
    initial_count = len(mock_db_connector.address)

    result = address_dao.delete_address(id_to_delete)

    assert result is True
    assert len(mock_db_connector.address) == initial_count - 1
    assert not any(addr["id_address"] == id_to_delete for addr in mock_db_connector.address)

def test_delete_address_non_existing(address_dao: AddressDAO):
    """Teste la suppression d'une adresse qui n'existe pas."""
    result = address_dao.delete_address(999)

    assert result is False

# test for errors
def test_find_address_by_id_error_handling(address_dao: AddressDAO, mock_db_connector):
    """Teste que find_address_by_id retourne None en cas d'erreur DB."""
    mock_db_connector.sql_query = lambda q, d, rt: exec('raise Exception("Simulated DB Error")') if "SELECT" in q else None

    result = address_dao.find_address_by_id(1)

    assert result is None

def test_find_all_addresses_error_handling(address_dao: AddressDAO, mock_db_connector):
    """Teste que find_all_addresses retourne une liste vide en cas d'erreur DB."""
    mock_db_connector.sql_query = lambda q, d, rt: exec('raise Exception("Simulated DB Error")') if "SELECT" in q else None

    result = address_dao.find_all_addresses()

    assert result == []

def test_add_address_error_handling(address_dao: AddressDAO, mock_db_connector):
    """Teste que add_address retourne None en cas d'erreur DB."""
    mock_db_connector.sql_query = lambda q, d, rt: exec('raise Exception("Simulated DB Error")') if "INSERT" in q else None
    new_address = Address(city="Test", postal_code=12345, street_name="Error", street_number="1")

    result = address_dao.add_address(new_address)

    assert result is None

def test_update_address_error_handling(address_dao: AddressDAO, mock_db_connector):
    """Teste que update_address retourne False en cas d'erreur DB."""
    mock_db_connector.sql_query = lambda q, d, rt: exec('raise Exception("Simulated DB Error")') if "UPDATE" in q else None
    address_to_update = Address(id_address=1, city='Lyon', postal_code=69000, street_name='Rue', street_number="1")

    result = address_dao.update_address(address_to_update)

    assert result is False

def test_delete_address_error_handling(address_dao: AddressDAO, mock_db_connector):
    """Teste que delete_address retourne False en cas d'erreur DB."""
    mock_db_connector.sql_query = lambda q, d, rt: exec('raise Exception("Simulated DB Error")') if "DELETE" in q else None

    result = address_dao.delete_address(1)

    assert result is False
