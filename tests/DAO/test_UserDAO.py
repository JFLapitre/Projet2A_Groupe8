from datetime import date
from typing import TYPE_CHECKING, Literal, Optional, Union

from src.DAO.userDAO import UserDAO
from src.Model.customer import Customer

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
            }
        ]
        self.next_id = 2

    def sql_query(
        self,
        query: str,
        data: Optional[Union[tuple, list, dict]] = None,
        return_type: Union[Literal["one"], Literal["all"], None] = "one",
    ):
        q = " ".join(query.lower().split())

        if "from fd.user" in q and "where u.id_user" in q:
            id_user = data.get("id_user")
            for u in self.users:
                if u["id_user"] == id_user:
                    return u
            return None

        if "from fd.user" in q and "where u.username" in q:
            username = data.get("username")
            for u in self.users:
                if u["username"] == username:
                    return u
            return None

        if "from fd.user" in q and "left join" in q and "where" not in q:
            if return_type == "all":
                return self.users
            else:
                return self.users[0]

        if q.startswith("insert into fd.user"):
            new_user = {
                "id_user": self.next_id,
                "user_type": data.get("user_type"),
                "username": data.get("username"),
                "password": data.get("password"),
                "sign_up_date": date.today(),
                "name": data.get("username"),
                "customer_phone": "0000000000",
                "driver_name": None,
                "driver_phone": None,
                "vehicle_type": None,
                "availability": None,
                "admin_name": None,
                "admin_phone": None,
                "salt": "random_salt",
                "hash_password": "random_hash",
            }
            self.users.append(new_user)
            self.next_id += 1
            return {"id_user": new_user["id_user"]}

        if "update fd.user" in q:
            if not data:
                raise Exception("no data provided")
            user_id = data.get("id_user")
            for u in self.users:
                if u["id_user"] == user_id:
                    u.update(data)
            return None
        
        if "update fd.customer" in q:
            if not data:
                raise Exception("no data provided")
            user_id = data.get("id_user")
            for u in self.users:
                if u["id_user"] == user_id:
                    u["customer_name"] = data.get("name") 
                    u["customer_phone"] = data.get("phone_number")
            return None

        if q.startswith("delete from fd.user"):
            id_user = data.get("id_user")
            self.users = [u for u in self.users if u["id_user"] != id_user]
            return None

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
    assert isinstance(users, list)  # Vérifie que le résultat est une liste
    assert len(users) > 0


def test_add_user():
    mock_db = MockDBConnector()
    user_DAO = UserDAO(mock_db)

    from src.Model.customer import Customer

    new_user = Customer(
        id_user=0,
        username="alice",
        password="secret",
        sign_up_date=date.today(),
        customer_name="Alice",
        phone_number="0123456789",
        salt="random_salt_value",
        hash_password="random_hash",
    )

    added_user = user_DAO.add_user(new_user)
    assert added_user is not None
    assert added_user.username == "alice"
    assert added_user.id_user != 0  # Vérifie que l'ID a été assigné
    # Vérifie que l'utilisateur a été ajouté dans le mock
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