import pytest
from datetime import date, datetime
from src.DAO.DBConnector import DBConnector
from src.utils.reset_database_test import ResetDatabaseTest

# Import des DAOs
from src.DAO.userDAO import UserDAO
from src.DAO.itemDAO import ItemDAO
from src.DAO.addressDAO import AddressDAO
from src.DAO.bundleDAO import BundleDAO
from src.DAO.orderDAO import OrderDAO

# Import des Modèles
from src.Model.customer import Customer
from src.Model.address import Address
from src.Model.item import Item
from src.Model.predefined_bundle import PredefinedBundle
from src.Model.order import Order

@pytest.fixture(scope="module")
def db_connector():
    """
    Crée une connexion réelle à la DB de test.
    Réinitialise la base de données avant de commencer les tests du module.
    """
    # 1. Réinitialisation propre de la BDD de test
    reset_tool = ResetDatabaseTest()
    reset_tool.lancer()

    # 2. Connexion en mode test (pointe vers le schema de test)
    connector = DBConnector(test=True)
    return connector

@pytest.fixture(scope="module")
def daos(db_connector):
    """
    Instancie tous les DAOs nécessaires avec le connecteur réel.
    CORRECTION : Utilisation d'arguments nommés pour les classes héritant de Pydantic BaseModel.
    """
    # Classes classiques (pas Pydantic) -> Arguments positionnels OK
    user_dao = UserDAO(db_connector)
    item_dao = ItemDAO(db_connector)

    # Classes Pydantic (AddressDAO, BundleDAO) -> Arguments nommés OBLIGATOIRES
    address_dao = AddressDAO(db_connector=db_connector)
    bundle_dao = BundleDAO(db_connector=db_connector, item_dao=item_dao)
    
    # OrderDAO (Pydantic) -> Arguments nommés
    order_dao = OrderDAO(
        db_connector=db_connector,
        user_dao=user_dao,
        item_dao=item_dao,
        address_dao=address_dao,
        bundle_dao=bundle_dao
    )
    
    return {
        "user": user_dao,
        "item": item_dao,
        "address": address_dao,
        "bundle": bundle_dao,
        "order": order_dao
    }

def test_integration_workflow_order(daos):
    """
    Test d'intégration : Création complète d'une commande
    1. Créer un User (Client)
    2. Créer une Adresse
    3. Créer 2 Items
    4. Créer un Bundle avec ces items
    5. Créer une Commande liée au client et à l'adresse
    """
    
    # --- 1. Création du User (Customer) ---
    new_customer = Customer(
        username="integration_user",
        hash_password="hashed_secure_pass",
        salt="random_salt",
        name="Integration Tester",
        phone_number="+33612345678",
        sign_up_date=date.today()
    )
    created_customer = daos["user"].add_user(new_customer)
    
    assert created_customer is not None
    assert created_customer.id_user is not None
    print(f"User created with ID: {created_customer.id_user}")

    # --- 2. Création de l'Adresse ---
    new_address = Address(
        city="TestCity",
        postal_code=12345,
        street_name="Integration Blvd",
        street_number="42"
    )
    created_address = daos["address"].add_address(new_address)
    
    assert created_address is not None
    assert created_address.id_address is not None
    print(f"Address created with ID: {created_address.id_address}")

    # --- 3. Création des Items ---
    item1 = Item(name="Burger Test", item_type="main", price=10.0, stock=100, availability=True)
    item2 = Item(name="Fries Test", item_type="side", price=5.0, stock=100, availability=True)
    
    created_item1 = daos["item"].add_item(item1)
    created_item2 = daos["item"].add_item(item2)
    
    assert created_item1.id_item is not None
    assert created_item2.id_item is not None

    # --- 4. Création d'un Bundle Prédéfini ---
    bundle = PredefinedBundle(
        name="Integration Menu",
        description="Full meal",
        price=12.0, 
        composition=[created_item1, created_item2]
    )
    
    created_bundle = daos["bundle"].add_predefined_bundle(bundle)
    
    assert created_bundle is not None
    assert created_bundle.id_bundle is not None
    assert len(created_bundle.composition) == 2
    print(f"Bundle created with ID: {created_bundle.id_bundle}")

    # --- 5. Création de la Commande ---
    # On ajoute les items du bundle à la commande
    new_order = Order(
        customer=created_customer,
        address=created_address,
        items=created_bundle.composition, 
        status="pending",
        price=created_bundle.price,
        order_date=datetime.now()
    )
    
    created_order = daos["order"].add_order(new_order)
    
    assert created_order is not None
    assert created_order.id_order is not None
    assert created_order.status == "pending"
    assert created_order.price == 12.0
    assert len(created_order.items) == 2
    print(f"Order created with ID: {created_order.id_order}")

    # --- 6. Vérification de lecture (Read) ---
    fetched_order = daos["order"].find_order_by_id(created_order.id_order)
    assert fetched_order.customer.username == "integration_user"
    assert fetched_order.address.city == "TestCity"