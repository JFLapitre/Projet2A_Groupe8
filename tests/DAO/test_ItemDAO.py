import pytest

from src.DAO.DBConnector import DBConnector
from src.DAO.itemDAO import ItemDAO
from src.Model.item import Item


@pytest.fixture
def item_dao():
    """Fixture pour créer une instance d'ItemDAO."""
    db_connector = DBConnector()
    return ItemDAO(db_connector)


def test_find_all_items(item_dao):
    """Test la récupération de tous les items."""
    items = item_dao.find_all_items()
    assert isinstance(items, list)
    assert len(items) > 0
    assert all(isinstance(item, Item) for item in items)


def test_find_item_by_id_existing(item_dao):
    """Test la recherche d'un item existant."""
    item = item_dao.find_item_by_id(1)
    assert item is not None
    assert isinstance(item, Item)
    assert item.id_item == 1


def test_find_item_by_id_non_existing(item_dao):
    """Test la recherche d'un item inexistant."""
    item = item_dao.find_item_by_id(9999)
    assert item is None


def test_add_item(item_dao):
    """Test l'ajout d'un nouvel item."""
    new_item = Item(id_item=None, name="Test Pizza", item_type="main", price=15.00)
    created_item = item_dao.add_item(new_item)

    assert created_item is not None
    assert created_item.id_item is not None
    assert created_item.name == "Test Pizza"
    assert created_item.price == 15.00

    # Nettoyage
    item_dao.delete_item(created_item.id_item)


def test_update_item(item_dao):
    """Test la mise à jour d'un item."""
    # Créer un item de test
    new_item = Item(id_item=None, name="Test Update", item_type="main", price=10.00)
    created_item = item_dao.add_item(new_item)

    # Modifier l'item
    created_item.name = "Test Updated"
    created_item.price = 12.00
    success = item_dao.update_item(created_item)

    assert success is True

    # Vérifier la modification
    updated_item = item_dao.find_item_by_id(created_item.id_item)
    assert updated_item.name == "Test Updated"
    assert updated_item.price == 12.00

    # Nettoyage
    item_dao.delete_item(created_item.id_item)


def test_delete_item(item_dao):
    """Test la suppression d'un item."""
    # Créer un item de test
    new_item = Item(id_item=None, name="Test Delete", item_type="main", price=10.00)
    created_item = item_dao.add_item(new_item)

    # Supprimer l'item
    success = item_dao.delete_item(created_item.id_item)
    assert success is True

    # Vérifier la suppression
    deleted_item = item_dao.find_item_by_id(created_item.id_item)
    assert deleted_item is None
