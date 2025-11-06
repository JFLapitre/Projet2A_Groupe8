from datetime import date
from typing import Any, Dict, List, Literal, Optional, Union

import pytest

from src.DAO.itemDAO import ItemDAO
from src.Model.item import Item


class MockDBConnector:
    """
    Mock de DBConnector pour simuler les opérations CRUD de ItemDAO
    directement dans le fichier de test.
    """

    def __init__(self):
        self.users = [{"id_user": 1, "username": "janjak", "user_type": "customer", "sign_up_date": date.today()}]

        self.items = [
            {
                "id_item": 1,
                "name": "Item Existant A",
                "item_type": "side",
                "price": 5.00,
                "description": "Un item de base",
                "stock": 50,
                "availability": True,
            },
            {
                "id_item": 2,
                "name": "Item Existant B",
                "item_type": "main",
                "price": 12.00,
                "description": "Un autre item de base",
                "stock": 25,
                "availability": True,
            },
        ]
        # Corrigé : L'ID suivant doit être 3, car 1 et 2 existent déjà.
        self.next_item_id = 3

    def sql_query(
        self,
        query: str,
        data: Optional[Union[tuple, list, dict]] = None,
        return_type: Optional[Union[Literal["one"], Literal["all"], None]] = "one",
    ) -> Union[Dict[str, Any], List[Dict[str, Any]], bool, None]:
        q = " ".join(query.lower().split())

        # add item
        # CORRIGÉ: "insert into item"
        if "insert into item" in q:
            if not isinstance(data, dict):
                return False

            new_id = self.next_item_id
            self.next_item_id += 1

            created_item = {
                "id_item": new_id,
                "name": data["name"],
                "item_type": data["item_type"],
                "price": data["price"],
                "description": data.get("description")
                if data.get("description") is not None
                else "Pas de description.",
                "stock": data.get("stock") if data.get("stock") is not None else 0,
                "availability": data.get("availability") if data.get("availability") is not None else True,
            }

            self.items.append(created_item)
            return created_item

        # find all items
        # CORRIGÉ: "select * from item"
        if "select * from item" in q and return_type == "all":
            return list(self.items)

        # find item by id
        # CORRIGÉ: "from item"
        if "from item" in q and "where id_item" in q and return_type == "one":
            item_id = None
            if isinstance(data, dict):
                item_id = data.get("id_item")
            elif isinstance(data, (list, tuple)):
                if data:
                    item_id = data[0]
            if item_id:
                for item in self.items:
                    if item["id_item"] == item_id:
                        return item.copy()
            return None

        # update item
        # CORRIGÉ: "update item"
        if "update item" in q and "where id_item" in q:
            item_id_to_update = data.get("id_item")
            for item in self.items:
                if item["id_item"] == item_id_to_update:
                    for key, value in data.items():
                        if key != "id_item":
                            item[key] = value
                    return True
            return False

        # delete item
        # CORRIGÉ: "delete from item"
        if "delete from item" in q and "where id_item" in q:
            item_id_to_delete = None
            if isinstance(data, dict):
                item_id_to_delete = data.get("id_item")
            elif isinstance(data, (list, tuple)):
                if data:
                    item_id_to_delete = data[0]
            if item_id_to_delete is None:
                return False
            initial_count = len(self.items)
            self.items = [item for item in self.items if item["id_item"] != item_id_to_delete]
            return len(self.items) < initial_count

        return None


@pytest.fixture
def item_dao():
    mock_connector = MockDBConnector()
    return ItemDAO(mock_connector)


def test_find_all_items(item_dao):
    """Test finding all item"""
    items = item_dao.find_all_items()
    assert isinstance(items, list)
    assert len(items) == 2
    assert all(isinstance(item, Item) for item in items)


def test_find_item_by_id_existing(item_dao):
    """Test the research of one item"""
    item = item_dao.find_item_by_id(1)
    assert item is not None
    assert isinstance(item, Item)
    assert item.id_item == 1


def test_find_item_by_id_non_existing(item_dao):
    """Test the research of one inexisting item"""
    item = item_dao.find_item_by_id(9999)
    assert item is None


def test_add_item(item_dao):
    """Test adding one item"""
    new_item = Item(id_item=None, name="Test Pizza", item_type="main", price=15.00)

    # Le MockDBConnector a next_item_id = 3
    created_item = item_dao.add_item(new_item)

    assert created_item is not None
    assert created_item.id_item == 3  # ID doit être 3
    assert created_item.name == "Test Pizza"
    assert created_item.price == 15.00

    item_dao.delete_item(created_item.id_item)


def test_update_item(item_dao):
    """Test the update of one item"""
    # Utilise l'item 1 existant pour la mise à jour
    item_to_update = item_dao.find_item_by_id(1)

    item_to_update.name = "Test Updated"
    item_to_update.price = 12.00
    success = item_dao.update_item(item_to_update)

    assert success is True

    updated_item = item_dao.find_item_by_id(1)
    assert updated_item.name == "Test Updated"
    assert updated_item.price == 12.00


def test_delete_item(item_dao):
    """Test deleting one item"""
    # Ajoute un item pour le supprimer (ID 3)
    new_item = Item(id_item=None, name="Test Delete", item_type="main", price=10.00)
    created_item = item_dao.add_item(new_item)
    assert created_item.id_item == 3

    success = item_dao.delete_item(created_item.id_item)
    assert success is True

    deleted_item = item_dao.find_item_by_id(created_item.id_item)
    assert deleted_item is None


def test_add_item_minimal_data(item_dao):
    """Test the add of one item without optionnal values"""
    new_item = Item(id_item=None, name="Minimal Side", item_type="side", price=3.50)
    created_item = item_dao.add_item(new_item)  # ID 3

    assert created_item is not None
    assert created_item.name == "Minimal Side"
    assert created_item.price == 3.50

    # Vérifie les valeurs par défaut définies dans le mock
    assert created_item.description == "Pas de description."
    assert created_item.stock == 0
    assert created_item.availability is True

    item_dao.delete_item(created_item.id_item)


def test_update_item_non_existing(item_dao):
    """Test the update of an inexisting item"""
    non_existing_item = Item(id_item=9997, name="Should not exist", item_type="side", price=1.00)
    success = item_dao.update_item(non_existing_item)
    assert success is False


def test_delete_item_non_existing(item_dao):
    """Test deleting an inexisting item"""
    success = item_dao.delete_item(9998)
    assert success is False
