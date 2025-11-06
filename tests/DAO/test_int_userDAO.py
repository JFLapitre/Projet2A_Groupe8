import os
from datetime import date

import pytest

from src.DAO.DBConnector import DBConnector
from src.DAO.userDAO import UserDAO
from src.Model.admin import Admin
from src.Model.customer import Customer
from src.Model.driver import Driver
from src.utils.reset_database_test import ResetDatabaseTest

# --- Fixtures d'Intégration ---


@pytest.fixture(scope="function", autouse=True)
def setup_database(monkeypatch):
    """
    Fixture automatique (autouse=True) pour réinitialiser la BDD de test
    avant CHAQUE test (scope="function").

    Elle utilise monkeypatch pour forcer le DBConnector à utiliser
    le schéma 'tests' en définissant la variable d'environnement.
    """

    # Force le DBConnector à utiliser le schéma 'tests'
    monkeypatch.setenv("POSTGRES_SCHEMA", "tests")

    # Lance le script de réinitialisation de la BDD de test
    reset_script = ResetDatabaseTest()
    success = reset_script.lancer()

    # Assure que la réinitialisation a réussi avant de lancer le test
    assert success is True, "Échec de la réinitialisation de la base de données de test."

    # Le test s'exécute ici
    yield

    # (Pas de nettoyage nécessaire après, car le prochain test réinitialisera à nouveau)


@pytest.fixture(scope="function")
def db_connector() -> DBConnector:
    """
    Fournit un VRAI connecteur de base de données pointant vers la BDD de test.
    Dépend implicitement de 'setup_database' (grâce à autouse=True)
    pour s'assurer que l'ENV VAR 'POSTGRES_SCHEMA' est positionnée sur 'tests'.
    """
    # load_dotenv() est appelé dans DBConnector, donc les vars sont chargées
    return DBConnector()


@pytest.fixture(scope="function")
def user_dao(db_connector: DBConnector) -> UserDAO:
    """
    Fournit une instance de UserDAO utilisant le vrai connecteur de BDD.
    """
    return UserDAO(db_connector)


# --- Tests des Méthodes DAO ---


def test_find_user_by_id(user_dao: UserDAO):
    """
    Teste la récupération d'utilisateurs par ID depuis la BDD de test.
    Les données proviennent de 'pop_db_test.sql'.
    """
    # 1. Tester un Customer (ID 1)
    customer = user_dao.find_user_by_id(1)
    assert customer is not None
    assert isinstance(customer, Customer)
    assert customer.username == "john_doe"
    assert customer.name == "John Doe"

    # 2. Tester un Driver (ID 3)
    driver = user_dao.find_user_by_id(3)
    assert driver is not None
    assert isinstance(driver, Driver)
    assert driver.username == "bob_driver"
    assert driver.vehicle_type == "Scooter"
    assert driver.availability is True

    # 3. Tester un Admin (ID 4)
    admin = user_dao.find_user_by_id(4)
    assert admin is not None
    assert isinstance(admin, Admin)
    assert admin.username == "alice_admin"
    assert admin.name == "Alice Admin"

    # 4. Tester un ID inexistant
    non_existent = user_dao.find_user_by_id(9999)
    assert non_existent is None


def test_find_user_by_username(user_dao: UserDAO):
    """
    Teste la récupération d'utilisateurs par username.
    Note : Le type hint 'int' dans le fichier source est une erreur,
    l'implémentation attend bien un 'str'.
    """
    # 1. Tester un Customer
    customer = user_dao.find_user_by_username("john_doe")
    assert customer is not None
    assert isinstance(customer, Customer)
    assert customer.id_user == 1

    # 2. Tester un Driver
    driver = user_dao.find_user_by_username("bob_driver")
    assert driver is not None
    assert isinstance(driver, Driver)
    assert driver.id_user == 3

    # 3. Tester un username inexistant
    non_existent = user_dao.find_user_by_username("nouser")
    assert non_existent is None


def test_find_all_no_filter(user_dao: UserDAO):
    """
    Teste la récupération de TOUS les utilisateurs.
    'pop_db_test.sql' insère 13 utilisateurs.
    """
    all_users = user_dao.find_all()
    assert all_users is not None
    assert isinstance(all_users, list)
    assert len(all_users) == 13

    # Vérifie qu'on a bien un mélange de types
    types_found = {type(user) for user in all_users}
    assert Customer in types_found
    assert Driver in types_found
    assert Admin in types_found


def test_find_all_filtered(user_dao: UserDAO):
    """
    Teste le filtre 'user_type' de la méthode find_all.
    Données de 'pop_db_test.sql':
    - 8 Customers (3 originaux + 5 nouveaux)
    - 3 Drivers (1 original + 2 nouveaux)
    - 2 Admins (1 original + 1 nouveau)
    """
    # 1. Filtre Customer
    customers = user_dao.find_all(user_type="customer")
    assert len(customers) == 8
    assert all(isinstance(c, Customer) for c in customers)

    # 2. Filtre Driver
    drivers = user_dao.find_all(user_type="driver")
    assert len(drivers) == 3
    assert all(isinstance(d, Driver) for d in drivers)

    # 3. Filtre Admin
    admins = user_dao.find_all(user_type="admin")
    assert len(admins) == 2
    assert all(isinstance(a, Admin) for a in admins)

    # 4. Filtre invalide
    invalid = user_dao.find_all(user_type="non_existent_type")
    assert len(invalid) == 0


def test_add_user_crud(user_dao: UserDAO):
    """
    Teste l'ajout (Create) d'un nouvel utilisateur et sa relecture (Read).
    La BDD de test contient 13 utilisateurs, le prochain ID sera 14.
    """
    # 1. Créer un nouveau Customer
    new_customer = Customer(
        username="new_test_customer",
        hash_password="testhash",
        salt="testsalt",
        sign_up_date=date.today(),
        name="Test Customer",
        phone_number="1234567890",
    )

    created_customer = user_dao.add_user(new_customer)

    # Vérifie l'objet retourné
    assert created_customer is not None
    assert isinstance(created_customer, Customer)
    assert created_customer.id_user == 14
    assert created_customer.username == "new_test_customer"
    assert created_customer.name == "Test Customer"

    # 2. Relire depuis la BDD pour confirmer
    read_customer = user_dao.find_user_by_id(14)
    assert read_customer is not None
    assert read_customer.name == "Test Customer"
    assert read_customer.phone_number == "1234567890"


def test_update_user_crud(user_dao: UserDAO):
    """
    Teste la mise à jour (Update) d'un utilisateur existant.
    """
    # 1. Récupérer un utilisateur (Driver ID 3)
    driver_to_update = user_dao.find_user_by_id(3)
    assert isinstance(driver_to_update, Driver)
    assert driver_to_update.availability is True
    assert driver_to_update.vehicle_type == "Scooter"

    # 2. Modifier l'objet
    driver_to_update.availability = False
    driver_to_update.vehicle_type = "Bicycle"
    driver_to_update.name = "Bob (Updated)"

    # 3. Appeler update_user
    updated_driver = user_dao.update_user(driver_to_update)

    # 4. Vérifier l'objet retourné
    assert updated_driver is not None
    assert updated_driver.id_user == 3
    assert updated_driver.availability is False
    assert updated_driver.vehicle_type == "Bicycle"

    # 5. Relire depuis la BDD pour confirmer
    read_driver = user_dao.find_user_by_id(3)
    assert isinstance(read_driver, Driver)
    assert read_driver.availability is False
    assert read_driver.vehicle_type == "Bicycle"
    assert read_driver.name == "Bob (Updated)"


def test_delete_user_crud(user_dao: UserDAO):
    """
    Teste la suppression (Delete) d'un utilisateur.
    """
    # 1. Vérifier que l'utilisateur (Customer ID 1) existe
    user_to_delete = user_dao.find_user_by_id(1)
    assert user_to_delete is not None

    # 2. Vérifier le nombre total d'utilisateurs (13)
    all_users_before = user_dao.find_all()
    assert len(all_users_before) == 13

    # 3. Supprimer l'utilisateur
    delete_success = user_dao.delete_user(1)
    assert delete_success is True

    # 4. Vérifier qu'il n'existe plus
    deleted_user = user_dao.find_user_by_id(1)
    assert deleted_user is None

    # 5. Vérifier que le nombre total a diminué
    all_users_after = user_dao.find_all()
    assert len(all_users_after) == 12
