import pytest
import psycopg2
from datetime import date, datetime
from src.DAO.DBConnector import DBConnector
from src.utils.reset_database_test import ResetDatabaseTest

from src.DAO.userDAO import UserDAO
from src.DAO.itemDAO import ItemDAO
from src.DAO.addressDAO import AddressDAO
from src.DAO.bundleDAO import BundleDAO
from src.DAO.orderDAO import OrderDAO
from src.DAO.deliveryDAO import DeliveryDAO

from src.Model.customer import Customer
from src.Model.driver import Driver
from src.Model.address import Address
from src.Model.item import Item
from src.Model.predefined_bundle import PredefinedBundle
from src.Model.order import Order
from src.Model.delivery import Delivery

@pytest.fixture(scope="module")
def db_connector():
    """
    Crée une connexion réelle à la DB de test.
    Réinitialise la base de données avant de commencer les tests du module.
    """
    reset_tool = ResetDatabaseTest()
    reset_tool.lancer()

    connector = DBConnector(test=True)
    return connector

@pytest.fixture(scope="module")
def daos(db_connector):
    """
    Instancie tous les DAOs nécessaires avec le connecteur réel.
    CORRECTION : Arguments nommés obligatoires pour les classes Pydantic.
    """
    user_dao = UserDAO(db_connector)
    item_dao = ItemDAO(db_connector)
    
    address_dao = AddressDAO(db_connector=db_connector)
    bundle_dao = BundleDAO(db_connector=db_connector, item_dao=item_dao)
    
    order_dao = OrderDAO(
        db_connector=db_connector,
        user_dao=user_dao,
        item_dao=item_dao,
        address_dao=address_dao,
        bundle_dao=bundle_dao
    )
    
    delivery_dao = DeliveryDAO(
        db_connector=db_connector,
        user_dao=user_dao,
        order_dao=order_dao
    )
    
    return {
        "user": user_dao,
        "item": item_dao,
        "address": address_dao,
        "bundle": bundle_dao,
        "order": order_dao,
        "delivery": delivery_dao
    }

def test_integration_workflow_order(daos):
    """
    Test : Création complète d'une commande (Client -> Adresse -> Items -> Bundle -> Commande)
    """
    new_customer = Customer(
        username="integration_user",
        hash_password="hashed_pass",
        salt="random_salt",
        name="Integration Tester",
        phone_number="+33612345678",
        sign_up_date=date.today()
    )
    created_customer = daos["user"].add_user(new_customer)
    assert created_customer.id_user is not None

    new_address = Address(
        city="TestCity",
        postal_code=12345,
        street_name="Integration Blvd",
        street_number="42"
    )
    created_address = daos["address"].add_address(new_address)
    assert created_address.id_address is not None

    item1 = Item(name="Burger Test", item_type="main", price=10.0, stock=100, availability=True)
    item2 = Item(name="Fries Test", item_type="side", price=5.0, stock=100, availability=True)
    created_item1 = daos["item"].add_item(item1)
    created_item2 = daos["item"].add_item(item2)

    bundle = PredefinedBundle(
        name="Integration Menu",
        description="Full meal",
        price=12.0, 
        composition=[created_item1, created_item2]
    )
    created_bundle = daos["bundle"].add_predefined_bundle(bundle)
    assert created_bundle.id_bundle is not None

    new_order = Order(
        customer=created_customer,
        address=created_address,
        items=created_bundle.composition, 
        status="pending",
        price=created_bundle.price,
        order_date=datetime.now()
    )
    created_order = daos["order"].add_order(new_order)
    
    assert created_order.id_order is not None
    assert created_order.status == "pending"
    assert len(created_order.items) == 2
    
    fetched_order = daos["order"].find_order_by_id(created_order.id_order)
    assert fetched_order.customer.username == "integration_user"

def test_integration_delivery_workflow(daos):
    """
    Test : Création d'un livreur et assignation d'une commande à une livraison.
    """
    driver = Driver(
        username="fast_driver",
        hash_password="pwd",
        salt="slt",
        name="Fast Eddie",
        phone_number="0700000000",
        vehicle_type="scooter",
        availability=True
    )
    created_driver = daos["user"].add_user(driver)
    assert isinstance(created_driver, Driver)

    customer = daos["user"].find_user_by_username("integration_user")
    address = daos["address"].find_all_addresses()[0]
    
    order_for_delivery = Order(
        customer=customer,
        address=address,
        items=[],
        status="validated",
        price=20.0,
        order_date=datetime.now()
    )
    created_order = daos["order"].add_order(order_for_delivery)

    delivery = Delivery(
        driver=created_driver,
        orders=[created_order],
        status="in_progress",
        delivery_time=None
    )
    created_delivery = daos["delivery"].add_delivery(delivery)

    assert created_delivery is not None
    assert created_delivery.id_delivery is not None
    assert created_delivery.driver.id_user == created_driver.id_user
    assert len(created_delivery.orders) == 1
    assert created_delivery.orders[0].id_order == created_order.id_order

    fetched_delivery = daos["delivery"].find_delivery_by_id(created_delivery.id_delivery)
    assert fetched_delivery.status == "in_progress"
    assert fetched_delivery.driver.name == "Fast Eddie"

def test_integration_cascade_delete(daos):
    """
    Test : Vérifie que la suppression d'un client supprime bien ses commandes (ON DELETE CASCADE).
    """
    temp_customer = Customer(
        username="temp_user",
        hash_password="pwd",
        salt="slt",
        name="Temp",
        phone_number="000"
    )
    created_temp = daos["user"].add_user(temp_customer)
    
    address = daos["address"].find_all_addresses()[0]
    order = Order(
        customer=created_temp,
        address=address,
        items=[],
        status="pending",
        price=10.0
    )
    created_order = daos["order"].add_order(order)
    order_id = created_order.id_order

    assert daos["order"].find_order_by_id(order_id) is not None

    daos["user"].delete_user(created_temp.id_user)

    assert daos["user"].find_user_by_id(created_temp.id_user) is None

    assert daos["order"].find_order_by_id(order_id) is None

def test_integration_unique_username(daos, db_connector):
    """
    Test : Vérifie qu'on ne peut pas créer deux utilisateurs avec le même username.
    """
    u1 = Customer(username="unique_one", hash_password="p", salt="s", name="U1", phone_number="1")
    daos["user"].add_user(u1)

    u2 = Customer(username="unique_one", hash_password="p", salt="s", name="U2", phone_number="2")
    
    result = daos["user"].add_user(u2)
    assert result is None