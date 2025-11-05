from datetime import date
from typing import TYPE_CHECKING, Literal, Optional, Union

from src.DAO.userDAO import UserDAO
from src.Model.customer import Customer
from src.Model.driver import Driver
from src.Model.admin import Admin

if TYPE_CHECKING:
    from src.Model.abstract_user import AbstractUser


class MockDBConnector:
    from datetime import date

    def __init__(self):
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
                "id_user": 2, # Assurez-vous d'utiliser un nouvel ID
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
            }
]
        self.next_id = 4

    def sql_query(
        self,
        query: str,
        data: Optional[Union[tuple, list, dict]] = None,
        return_type: Union[Literal["one"], Literal["all"], None] = "one",
    ):
        q = " ".join(query.lower().split())

        # to find user by id
        if "from fd.user" in q and "where u.id_user" in q:
            id_user = data.get("id_user")
            for u in self.users:
                if u["id_user"] == id_user:
                    return u
            return None

        # to find user by username
        if "from fd.user" in q and "where u.username" in q:
            username = data.get("username")
            for u in self.users:
                if u["username"] == username:
                    return u
            return None

        # to find all users
        if "from fd.user" in q and "left join" in q and "where" not in q:
            if return_type == "all":
                return self.users
            else:
                return self.users[0]

        if "from fd.user" in q and "left join" in q and "where u.user_type" in q:
            user_type = data.get("user_type")
            filtered_users = [u for u in self.users if u["user_type"] == user_type]
            if return_type == "all":
                return filtered_users
            else:
                return filtered_users[0] if filtered_users else None

        # to add user
        if q.startswith("insert into fd.user"):
            new_id = self.next_id
            user_type = data.get("user_type")

            new_user = {
                "id_user": new_id,
                "user_type": user_type,
                "username": data.get("username"),
                "password": data.get("password"),
                "sign_up_date": date.today(),
                "salt": "random_salt",
                "hash_password": "random_hash",
                "customer_name": None, "customer_phone": None,
                "driver_name": None, "driver_phone": None, "vehicle_type": None, "availability": False,
                "admin_name": None, "admin_phone": None,
            }

            if user_type == "driver":
                new_user["driver_name"] = "Default Driver Name"
                new_user["driver_phone"] = "0000000000"
                new_user["vehicle_type"] = "Car"
            if user_type == "customer":
                new_user["customer_name"] = "Default Customer Name"
                new_user["customer_phone"] = "0000000000"
            if user_type == "admin":
                new_user["admin_name"] = "Default Admin Name"
                new_user["admin_phone"] = "0000000000"

            self.users.append(new_user)
            self.next_id += 1

            return {"id_user": new_user["id_user"]}

        if q.startswith("insert into fd.driver"):
            id_user = data.get("id_user")
            for u in self.users:
                if u["id_user"] == id_user:
                    u["driver_name"] = data.get("name")
                    u["driver_phone"] = data.get("phone_number")
                    u["vehicle_type"] = data.get("vehicle_type")
                    u["availability"] = data.get("availability") 
            return None

        if q.startswith("insert into fd.customer"):
            id_user = data.get("id_user")
            for u in self.users:
                if u["id_user"] == id_user:
                    u["customer_name"] = data.get("name")
                    u["customer_phone"] = data.get("phone_number")
            return None

        if q.startswith("insert into fd.admin"):
            id_user = data.get("id_user")
            for u in self.users:
                if u["id_user"] == id_user:
                    u["admin_name"] = data.get("name")
                    u["admin_phone"] = data.get("phone_number")
            return None

        # to update user
        if "update fd.user" in q:
            if not data:
                raise Exception("no data provided")
            user_id = data.get("id_user")
            for u in self.users:
                if u["id_user"] == user_id:
                    u.update(data)
            return None
        # to update customer
        if "update fd.customer" in q:
            if not data:
                raise Exception("no data provided")
            user_id = data.get("id_user")
            for u in self.users:
                if u["id_user"] == user_id:
                    u["customer_name"] = data.get("name")
                    u["customer_phone"] = data.get("phone_number")
            return None
        # to update driver
        if "update fd.driver" in q:
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
        if "update fd.admin" in q:
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
        if q.startswith("delete from fd.customer"):
            return None
        elif q.startswith("delete from fd.driver"):
            return None
        elif q.startswith("delete from fd.admin"):
            return None

        if q.startswith("delete from fd.user"):
            id_user_to_delete = data.get("id_user")

            if id_user_to_delete is not None:
                id_user_to_delete = int(id_user_to_delete)

                self.users = [u for u in self.users if u["id_user"] != id_user_to_delete]

        return None

def test_find_user_by_id():
    user_DAO = UserDAO(MockDBConnector())
    user: AbstractUser = user_DAO.find_user_by_id(1)
    assert user is not None
    assert user.id_user == 1
    assert user.username == "janjak"


def test_find_user_by_username():
    user_DAO = UserDAO(MockDBConnector())
    user: AbstractUser = user_DAO.find_user_by_username("janjak")
    assert user is not None
    assert user.id_user == 1
    assert user.username == "janjak"


def test_find_all():
    user_DAO = UserDAO(MockDBConnector())
    users: list[AbstractUser] = user_DAO.find_all()
    assert users is not None
    assert isinstance(users, list)
    assert len(users) > 0


def test_add_user():
    mock_db = MockDBConnector()
    user_DAO = UserDAO(mock_db)

    new_user = Customer(
        id_user=0,
        username="alice",
        password="secret",
        sign_up_date=date.today(),
        name="Alice",
        phone_number="0123456789",
        salt="random_salt_value",
        hash_password="random_hash",
    )

    added_user = user_DAO.add_user(new_user)
    assert added_user is not None
    assert added_user.username == "alice"
    assert added_user.id_user != 0
    assert any(u["username"] == "alice" for u in mock_db.users)

def test_update_user():
    mock_db = MockDBConnector()
    user_DAO = UserDAO(mock_db)

    existing_user = user_DAO.find_user_by_id(1)
    assert existing_user is not None, "L'utilisateur initial doit exister"

    updated_user = Customer(
        id_user=1,
        username="janjak_updated",
        hash_password="newSecret",
        salt="random_salt",
        password="newSecret",
        sign_up_date=date.today(),
        name="Jean Updated",
        phone_number="0000000001"
    )

    user_DAO.update_user(updated_user)

    modified_user = user_DAO.find_user_by_id(1)

    assert modified_user is not None
    assert modified_user.username == "janjak_updated"
    assert modified_user.name == "Jean Updated"
    assert modified_user.phone_number == "0000000001"
    assert modified_user.salt == "random_salt"
    assert modified_user.hash_password == "newSecret"

def test_delete_user():
    mock_db = MockDBConnector()
    user_DAO = UserDAO(mock_db)

    id_to_delete = 1
    existing_user = user_DAO.find_user_by_id(1)
    assert existing_user is not None, "L'utilisateur initial doit exister"

    initial_count = len(mock_db.users)
    assert initial_count > 0

    delete = user_DAO.delete_user(id_to_delete)
    assert delete is True, "La suppression doit retourner True"

    deleted_user = user_DAO.find_user_by_id(id_to_delete)
    assert deleted_user is None, "L'utilisateur ne doit plus être trouvé après la suppression"

    final_count = len(mock_db.users)
    assert final_count == initial_count - 1

def test_find_all_filtered_drivers():
    user_DAO = UserDAO(MockDBConnector())
    drivers = user_DAO.find_all(user_type="driver")

    assert len(drivers) == 1
    assert drivers[0].username == "driver_bob"
    assert isinstance(drivers[0], Driver)

def test_find_driver_by_id():
    """Vérifie la récupération et l'instanciation correcte d'un objet Driver."""
    user_DAO = UserDAO(MockDBConnector())

    driver: Driver = user_DAO.find_user_by_id(2)

    assert driver is not None
    assert isinstance(driver, Driver)
    assert driver.username == "driver_bob"
    assert driver.name == "Bob Driver"
    assert driver.vehicle_type == "Truck"
    assert driver.availability is True

def test_add_driver():
    """Vérifie l'ajout d'un nouvel utilisateur de type Driver."""
    mock_db = MockDBConnector()
    user_DAO = UserDAO(mock_db)

    new_driver = Driver(
        id_user=0,
        username="driver_sue",
        password="secret_sue",
        sign_up_date=date.today(),
        name="Sue Driver",
        phone_number="5555555555",
        salt="salt_sue",
        hash_password="hash_sue",
        vehicle_type="Bike",
        availability=False
    )

    added_driver = user_DAO.add_user(new_driver)

    assert added_driver is not None
    assert added_driver.username == "driver_sue"
    assert added_driver.vehicle_type == "Bike"
    assert added_driver.availability is False
    assert any(u["username"] == "driver_sue" for u in mock_db.users)

def test_update_driver():
    """Vérifie la mise à jour des informations d'un Driver."""
    mock_db = MockDBConnector()
    user_DAO = UserDAO(mock_db)

    existing_driver = user_DAO.find_user_by_id(2)
    assert existing_driver.vehicle_type == "Truck"

    updated_driver_data = Driver(
        id_user=2,
        username="bob_updated",
        hash_password="new_hash",
        salt="new_salt",
        password="new_pw",
        sign_up_date=date.today(),
        name="Bob Updated",
        phone_number="2222222222",
        vehicle_type="Van",
        availability=False
    )

    user_DAO.update_user(updated_driver_data)

    modified_driver = user_DAO.find_user_by_id(2)

    assert modified_driver is not None
    assert modified_driver.username == "bob_updated"
    assert modified_driver.name == "Bob Updated"
    assert modified_driver.vehicle_type == "Van"
    assert modified_driver.availability is False

def test_add_admin():
    """Vérifie l'ajout d'un nouvel utilisateur de type Admin."""
    mock_db = MockDBConnector()
    user_DAO = UserDAO(mock_db)

    new_admin = Admin(
        id_user=0,
        username="new_chief",
        password="secure_admin",
        sign_up_date=date.today(),
        name="Chief New",
        phone_number="3333333333",
        salt="salt_admin",
        hash_password="hash_admin",
    )

    added_admin = user_DAO.add_user(new_admin)

    assert added_admin is not None
    assert isinstance(added_admin, Admin)
    assert added_admin.username == "new_chief"
    assert added_admin.id_user != 0
    assert any(u["username"] == "new_chief" for u in mock_db.users)


def test_update_admin():
    """Vérifie la mise à jour des informations d'un Admin."""
    mock_db = MockDBConnector()
    user_DAO = UserDAO(mock_db)

    existing_admin = user_DAO.find_user_by_id(3)
    assert existing_admin.username == "super_admin"

    updated_admin_data = Admin(
        id_user=3,
        username="super_admin_v2",
        hash_password="new_admin_hash",
        salt="new_admin_salt",
        password="new_pw",
        sign_up_date=date.today(),
        name="Chief Admin Updated",
        phone_number="4444444444",
    )

    user_DAO.update_user(updated_admin_data)

    modified_admin = user_DAO.find_user_by_id(3)

    assert modified_admin is not None
    assert isinstance(modified_admin, Admin)
    assert modified_admin.username == "super_admin_v2"
    assert modified_admin.name == "Chief Admin Updated"
    assert modified_admin.phone_number == "4444444444"


def test_find_all_filtered_admins():
    """Vérifie la récupération de tous les utilisateurs de type Admin."""
    user_DAO = UserDAO(MockDBConnector())
    admins = user_DAO.find_all(user_type="admin")
    
    assert len(admins) == 1
    assert admins[0].username == "super_admin"
    assert isinstance(admins[0], Admin)

#Error tests
def test_find_user_by_id_error():
    class ErrorMock(MockDBConnector):
        def sql_query(self, query, data, return_type):
            if "where u.id_user" in query.lower():
                raise Exception("Simulated DB Error")
            return super().sql_query(query, data, return_type)

    user_DAO = UserDAO(ErrorMock())
    user = user_DAO.find_user_by_id(1)
    assert user is None

def test_find_user_by_username_error():
    """Test the error handling in find_user_by_username."""
    class ErrorMock(MockDBConnector):
        def sql_query(self, query, data, return_type):
            if "where u.username" in query.lower():
                raise Exception("Simulated DB Error")
            return super().sql_query(query, data, return_type)

    user_DAO = UserDAO(ErrorMock())
    user = user_DAO.find_user_by_username("janjak")
    assert user is None

def test_find_all_error():
    """Test the error handling in find_all."""
    class ErrorMock(MockDBConnector):
        def sql_query(self, query, data, return_type):
            if "from fd.user" in query.lower() and return_type == "all":
                if "where" not in query.lower() or "where u.user_type" in query.lower():
                    raise Exception("Simulated DB Error")
            return super().sql_query(query, data, return_type)

    user_DAO = UserDAO(ErrorMock())
    users = user_DAO.find_all()
    assert users == []

def test_update_user_error():
    """Test the error handling in update_user."""
    class ErrorMock(MockDBConnector):
        def sql_query(self, query, data, return_type):
            if "update fd.user" in query.lower():
                raise Exception("Simulated DB Error")
            return super().sql_query(query, data, return_type)

    user_DAO = UserDAO(ErrorMock())
    error_user = Customer(id_user=1, username="fail_update", hash_password="h", salt="s", name="N", phone_number="0")

    updated_user = user_DAO.update_user(error_user)
    assert updated_user is None

def test_delete_user_error():
    """Test the error handling in delete_user."""
    class ErrorMock(MockDBConnector):
        def sql_query(self, query, data, return_type):
            if query.lower().startswith("delete from fd.user"):
                raise Exception("Simulated DB Error")
            return super().sql_query(query, data, return_type)

    user_DAO = UserDAO(ErrorMock())
    success = user_DAO.delete_user(1)
    assert success is False

def test_add_user_error():
    """Test la gestion des erreurs lors de l'ajout d'un utilisateur."""
    class ErrorMock(MockDBConnector):
        def sql_query(self, query, data, return_type):
            # Simule une erreur uniquement sur la première insertion RETURNING id_user
            if "insert into fd.user" in query.lower() and "returning id_user" in query.lower():
                raise Exception("Simulated DB Insertion Error")
            # Le reste des requêtes utilise le Mock normal
            return super().sql_query(query, data, return_type)

    user_DAO = UserDAO(ErrorMock())
    new_user = Customer(
        id_user=0,
        username="error_user",
        hash_password="h", salt="s", name="N", phone_number="0",
        sign_up_date=date.today()
    )

    added_user = user_DAO.add_user(new_user)
    assert added_user is None