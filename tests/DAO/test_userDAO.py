from datetime import date
from typing import TYPE_CHECKING, Literal, Optional, Union

# Importation de pytest pour les fixtures
import pytest

from src.DAO.userDAO import UserDAO
from src.Model.admin import Admin
from src.Model.customer import Customer
from src.Model.driver import Driver

if TYPE_CHECKING:
    from src.Model.abstract_user import AbstractUser


class MockDBConnector:
    """Mock pour simuler les interactions avec la base de données."""

    def __init__(self):
        # Initialisation des données simulées
        self.users = [
            {
                "id_user": 1,
                "user_type": "customer",
                "username": "janjak",
                "password": "myHashedPassword",
                "sign_up_date": date.today(),
                "customer_name": "Jean",
                "customer_phone": "0000000000",
                "driver_name": None,
                "driver_phone": None,
                "vehicle_type": None,
                "availability": None,
                "admin_name": None,
                "admin_phone": None,
                "hash_password": "random_hash",
                "salt": "random_salt",
            },
            {
                "id_user": 2,
                "user_type": "driver",
                "username": "driver_bob",
                "password": "driverHashedPassword",
                "sign_up_date": date.today(),
                "customer_name": None,
                "customer_phone": None,
                "driver_name": "Bob Driver",
                "driver_phone": "1111111111",
                "vehicle_type": "Truck",
                "availability": True,
                "admin_name": None,
                "admin_phone": None,
                "hash_password": "random_driver_hash",
                "salt": "random_driver_salt",
            },
            # Nouvel Admin
            {
                "id_user": 3,
                "user_type": "admin",
                "username": "super_admin",
                "password": "adminHashedPassword",
                "sign_up_date": date.today(),
                "customer_name": None,
                "customer_phone": None,
                "driver_name": None,
                "driver_phone": None,
                "vehicle_type": None,
                "availability": None,
                "admin_name": "Chief Admin",
                "admin_phone": "9999999999",
                "hash_password": "random_admin_hash",
                "salt": "random_admin_salt",
            },
        ]
        self.next_id = 4
        # Flag pour simuler l'échec d'une requête spécifique (pour les tests d'erreur)
        self.raise_exception = False

    def sql_query(
        self,
        query: str,
        data: Optional[Union[tuple, list, dict]] = None,
        return_type: Union[Literal["one"], Literal["all"], None] = "one",
    ):
        q = " ".join(query.lower().split())

        # Gestion des erreurs simulées
        if self.raise_exception:
            if "where u.id_user" in q and 'from "user"' in q:
                if data and data.get("id_user") == 1:
                    raise Exception("Simulated DB Error (find by id)")
            if "where u.username" in q and 'from "user"' in q:
                if data and data.get("username") == "janjak":
                    raise Exception("Simulated DB Error (find by username)")
            if 'from "user"' in q and "left join" in q and return_type == "all":
                if "where" not in q or "where u.user_type" in q:
                    raise Exception("Simulated DB Error (find all)")
            if 'update "user"' in q:
                if data and data.get("id_user") == 1:
                    raise Exception("Simulated DB Error (update user)")
            if "update driver" in q:
                if data and data.get("id_user") == 2:
                    raise Exception("Simulated Child DB Update Error")
            if q.startswith('delete from "user"') and data and data.get("id_user") == 1:
                raise Exception("Simulated DB Error (delete user)")

        # to find user by id
        if 'from "user"' in q and "where u.id_user" in q:
            id_user = data.get("id_user")
            for u in self.users:
                if u["id_user"] == id_user:
                    return u
            return None

        # to find user by username
        if 'from "user"' in q and "where u.username" in q:
            username = data.get("username")
            for u in self.users:
                if u["username"] == username:
                    return u
            return None

        # to find all users
        if 'from "user"' in q and "left join" in q and "where" not in q:
            if return_type == "all":
                return self.users
            else:
                return self.users[0]

        # to find all users filtered
        if 'from "user"' in q and "left join" in q and "where u.user_type" in q:
            user_type = data.get("user_type")
            filtered_users = [u for u in self.users if u["user_type"] == user_type]
            if return_type == "all":
                return filtered_users
            else:
                return filtered_users[0] if filtered_users else None

        # to add user
        if q.startswith('insert into "user"'):
            new_id = self.next_id
            user_type = data.get("user_type")

            new_user = {
                "id_user": new_id,
                "user_type": user_type,
                "username": data.get("username"),
                "password": data.get("password"),
                "sign_up_date": date.today(),
                "salt": data.get("salt"),  # Assurer que le salt est pris en compte
                "hash_password": data.get("hash_password"),  # Assurer que le hash est pris en compte
                "customer_name": None,
                "customer_phone": None,
                "driver_name": None,
                "driver_phone": None,
                "vehicle_type": None,
                "availability": False,
                "admin_name": None,
                "admin_phone": None,
            }

            self.users.append(new_user)
            self.next_id += 1

            return {"id_user": new_user["id_user"]}

        # insert into driver
        if q.startswith("insert into driver"):
            id_user = data.get("id_user")
            for u in self.users:
                if u["id_user"] == id_user:
                    u["driver_name"] = data.get("name")
                    u["driver_phone"] = data.get("phone_number")
                    u["vehicle_type"] = data.get("vehicle_type")
                    u["availability"] = data.get("availability")
            return None

        # insert into customer
        if q.startswith("insert into customer"):
            id_user = data.get("id_user")
            for u in self.users:
                if u["id_user"] == id_user:
                    u["customer_name"] = data.get("name")
                    u["customer_phone"] = data.get("phone_number")
            return None

        # insert into admin
        if q.startswith("insert into admin"):
            id_user = data.get("id_user")
            for u in self.users:
                if u["id_user"] == id_user:
                    u["admin_name"] = data.get("name")
                    u["admin_phone"] = data.get("phone_number")
            return None

        # to update user
        if 'update "user"' in q:
            if not data:
                raise Exception("no data provided")
            user_id = data.get("id_user")
            for u in self.users:
                if u["id_user"] == user_id:
                    u["username"] = data.get("username")
                    u["hash_password"] = data.get("hash_password")
                    u["user_type"] = data.get("user_type")
                    # Ajouté la mise à jour de salt pour la couverture de test
                    if "salt" in data:
                        u["salt"] = data.get("salt")
            return None

        # to update customer
        if "update customer" in q:
            if not data:
                raise Exception("no data provided")
            user_id = data.get("id_user")
            for u in self.users:
                if u["id_user"] == user_id:
                    u["customer_name"] = data.get("name")
                    u["customer_phone"] = data.get("phone_number")
            return None

        # to update driver
        if "update driver" in q:
            if not data:
                raise Exception("no data provided")
            user_id = data.get("id_user")
            for u in self.users:
                if u["id_user"] == user_id:
                    u["driver_name"] = data.get("name")
                    u["driver_phone"] = data.get("phone_number")
                    u["vehicle_type"] = data.get("vehicle_type")
                    u["availability"] = data.get("availability")
            return None

        # to update admin
        if "update admin" in q:
            if not data:
                raise Exception("no data provided")
            user_id = data.get("id_user")

            if user_id is not None:
                user_id = int(user_id)

            for u in self.users:
                if u["id_user"] == user_id:
                    u["admin_name"] = data.get("name")
                    u["admin_phone"] = data.get("phone_number")
            return None

        # to delete user
        if q.startswith("delete from customer"):
            return None
        elif q.startswith("delete from driver"):
            return None
        elif q.startswith("delete from admin"):
            return None

        # delete from "user"
        if q.startswith('delete from "user"'):
            id_user_to_delete = data.get("id_user")

            if id_user_to_delete is not None:
                id_user_to_delete = int(id_user_to_delete)

                self.users = [u for u in self.users if u["id_user"] != id_user_to_delete]

        return None


# --- FIXTURES PYTEST ---


@pytest.fixture
def mock_db():
    """Fournit une instance réutilisable du MockDBConnector."""
    return MockDBConnector()


@pytest.fixture
def user_dao(mock_db):
    """Fournit une instance de UserDAO avec le MockDBConnector."""
    return UserDAO(mock_db)


# --- TESTS NOMINAUX ---


def test_find_user_by_id(user_dao: UserDAO):
    user: AbstractUser = user_dao.find_user_by_id(1)
    assert user is not None
    assert user.id_user == 1
    assert user.username == "janjak"
    assert isinstance(user, Customer)


def test_find_user_by_username(user_dao: UserDAO):
    user: AbstractUser = user_dao.find_user_by_username("janjak")
    assert user is not None
    assert user.id_user == 1
    assert user.username == "janjak"
    assert isinstance(user, Customer)


def test_find_all(user_dao: UserDAO):
    users: list[AbstractUser] = user_dao.find_all()
    assert users is not None
    assert isinstance(users, list)
    assert len(users) == 3


def test_add_customer(user_dao: UserDAO, mock_db: MockDBConnector):
    new_user = Customer(
        id_user=0,
        username="alice",
        hash_password="random_hash",
        salt="random_salt_value",
        sign_up_date=date.today(),
        name="Alice",
        phone_number="0123456789",
    )

    added_user = user_dao.add_user(new_user)
    assert added_user is not None
    assert added_user.username == "alice"
    assert added_user.id_user == 4  # Vérifie le nouvel ID
    assert any(u["username"] == "alice" for u in mock_db.users)
    assert isinstance(added_user, Customer)


def test_add_driver(user_dao: UserDAO, mock_db: MockDBConnector):
    new_driver = Driver(
        id_user=0,
        username="trucker_mike",
        hash_password="driver_hash",
        salt="driver_salt",
        sign_up_date=date.today(),
        name="Mike",
        phone_number="1234567890",
        vehicle_type="Van",
        availability=False,
    )

    added_driver = user_dao.add_user(new_driver)
    assert added_driver is not None
    assert added_driver.username == "trucker_mike"
    assert isinstance(added_driver, Driver)
    assert added_driver.vehicle_type == "Van"


def test_add_admin(user_dao: UserDAO, mock_db: MockDBConnector):
    new_admin = Admin(
        id_user=0,
        username="new_chief",
        hash_password="admin_hash",
        salt="admin_salt",
        sign_up_date=date.today(),
        name="New Chief",
        phone_number="1122334455",
    )

    added_admin = user_dao.add_user(new_admin)
    assert added_admin is not None
    assert added_admin.username == "new_chief"
    assert isinstance(added_admin, Admin)


def test_update_customer(user_dao: UserDAO):
    existing_user = user_dao.find_user_by_id(1)
    assert existing_user is not None, "L'utilisateur initial doit exister"

    updated_user = Customer(
        id_user=1,
        username="janjak_updated",
        hash_password=existing_user.hash_password,
        salt=existing_user.salt,
        sign_up_date=date.today(),
        name="Jean Updated",
        phone_number="0000000001",
    )

    user_dao.update_user(updated_user)

    modified_user = user_dao.find_user_by_id(1)

    assert modified_user is not None
    assert modified_user.username == "janjak_updated"
    assert modified_user.name == "Jean Updated"
    assert modified_user.phone_number == "0000000001"


def test_update_driver(user_dao: UserDAO):
    existing_driver = user_dao.find_user_by_id(2)
    assert isinstance(existing_driver, Driver)

    updated_driver = Driver(
        id_user=2,
        username="driver_bob_updated",
        hash_password="driver_h",
        salt="driver_s",
        password="p",
        sign_up_date=date.today(),
        name="Bob Driver Updated",
        phone_number="2222222222",
        vehicle_type="Van",
        availability=False,
    )

    user_dao.update_user(updated_driver)
    modified_driver = user_dao.find_user_by_id(2)

    assert isinstance(modified_driver, Driver)
    assert modified_driver.name == "Bob Driver Updated"
    assert modified_driver.phone_number == "2222222222"
    assert modified_driver.vehicle_type == "Van"
    assert modified_driver.availability is False


def test_update_admin(user_dao: UserDAO):
    existing_admin = user_dao.find_user_by_id(3)
    assert isinstance(existing_admin, Admin)

    updated_admin = Admin(
        id_user=3,
        username="super_admin_updated",
        hash_password="admin_h",
        salt="admin_s",
        sign_up_date=date.today(),
        name="Chief Admin Updated",
        phone_number="8888888888",
    )

    user_dao.update_user(updated_admin)
    modified_admin = user_dao.find_user_by_id(3)

    assert isinstance(modified_admin, Admin)
    assert modified_admin.name == "Chief Admin Updated"
    assert modified_admin.phone_number == "8888888888"


def test_delete_user(user_dao: UserDAO, mock_db: MockDBConnector):
    id_to_delete = 1
    existing_user = user_dao.find_user_by_id(1)
    assert existing_user is not None, "L'utilisateur initial doit exister"

    initial_count = len(mock_db.users)
    assert initial_count > 0

    delete = user_dao.delete_user(id_to_delete)
    assert delete is True, "La suppression doit retourner True"

    deleted_user = user_dao.find_user_by_id(id_to_delete)
    assert deleted_user is None, "L'utilisateur ne doit plus être trouvé après la suppression"

    final_count = len(mock_db.users)
    assert final_count == initial_count - 1


def test_find_all_filtered_drivers(user_dao: UserDAO):
    drivers = user_dao.find_all(user_type="driver")

    assert len(drivers) == 1
    assert drivers[0].username == "driver_bob"
    assert isinstance(drivers[0], Driver)


# --- TESTS D'ERREUR ET DE CAS LIMITES ---


def test_find_user_by_id_error(mock_db: MockDBConnector, user_dao: UserDAO):
    mock_db.raise_exception = True
    user = user_dao.find_user_by_id(1)
    assert user is None
    mock_db.raise_exception = False


def test_find_user_by_username_error(mock_db: MockDBConnector, user_dao: UserDAO):
    mock_db.raise_exception = True
    user = user_dao.find_user_by_username("janjak")
    assert user is None
    mock_db.raise_exception = False


def test_find_all_error(mock_db: MockDBConnector, user_dao: UserDAO):
    mock_db.raise_exception = True
    users = user_dao.find_all()
    assert users == []
    mock_db.raise_exception = False


def test_update_user_error(mock_db: MockDBConnector, user_dao: UserDAO):
    """Test the error handling in update_user (general table update failure)."""
    mock_db.raise_exception = True
    error_user = Customer(id_user=1, username="fail_update", hash_password="h", salt="s", name="N", phone_number="0")

    updated_user = user_dao.update_user(error_user)
    assert updated_user is None
    mock_db.raise_exception = False


def test_delete_user_error(mock_db: MockDBConnector, user_dao: UserDAO):
    """Test the error handling in delete_user."""
    mock_db.raise_exception = True
    success = user_dao.delete_user(1)
    assert success is False
    mock_db.raise_exception = False


def test_find_user_by_id_not_found(user_dao: UserDAO):
    """Checks that find_user_by_id returns None for a non-existent ID."""
    user = user_dao.find_user_by_id(999)  # ID non présent
    assert user is None


def test_find_user_by_username_not_found(user_dao: UserDAO):
    """Verifies that find_user_by_username returns None for a non-existent name."""
    user = user_dao.find_user_by_username("non_existent")
    assert user is None


def test_find_all_filtered_empty(user_dao: UserDAO):
    """Vérifie que find_all avec un filtre retourne une liste vide si aucun résultat."""
    # Le MockDBConnector actuel contient des Customers, Drivers et Admins.
    # On choisit un type non existant pour le test.
    users = user_dao.find_all(user_type="manager")
    assert users == []
    assert len(users) == 0


def test_update_driver_error_on_child_query(mock_db: MockDBConnector, user_dao: UserDAO):
    """
    Test la gestion d'erreur si la requête UPDATE "user" réussit
    mais la requête UPDATE driver échoue (simulé par le Mock).
    """
    mock_db.raise_exception = True  # Active l'erreur pour la requête 'update driver'

    # Données à jour pour le Driver (ID 2)
    updated_driver_data = Driver(
        id_user=2,
        username="bob_fail_update",
        hash_password="h",
        salt="s",
        password="p",
        sign_up_date=date.today(),
        name="Bob",
        phone_number="1",
        vehicle_type="Van",
        availability=True,
    )

    updated_user = user_dao.update_user(updated_driver_data)

    # L'update complet doit échouer si l'update enfant échoue.
    assert updated_user is None

    # Réinitialisation
    mock_db.raise_exception = False
