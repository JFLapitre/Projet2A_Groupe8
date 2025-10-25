from datetime import date
from typing import TYPE_CHECKING, Literal, Optional, Union

from src.DAO.userDAO import UserDAO

if TYPE_CHECKING:
    from src.Model.abstract_user import AbstractUser


class MockDBConnector:
    def sql_query(
        self,
        query: str,
        data: Optional[Union[tuple, list, dict]] = None,
        return_type: Union[Literal["one"], Literal["all"], None] = "one",
    ):
        # normalize query (remove extra whitespace, lowercase) to match the DAO's multi-line SQL
        q = " ".join(query.lower().split())

        # match the find_user_by_id query (FROM fd.user ... WHERE u.id_user = %(id_user)s)
        if "from fd.user" in q and "where u.id_user" in q:
            if not data:
                raise Exception("no data provided")
            if isinstance(data, dict):
                id_user = data.get("id_user")
            elif isinstance(data, (list, tuple)):
                id_user = data[0]
            else:
                id_user = data

            return {
                "id_user": id_user,
                "user_type": "customer",
                "username": "janjak",
                "password": "myHashedPassword",
                "sign_up_date": date.today(),
                "customer_name": "janjak",
                "customer_phone": "0000000000",
                "driver_name": None,
                "driver_phone": None,
                "vehicle_type": None,
                "availability": None,
                "admin_name": None,
                "admin_phone": None,
            }

        if "from fd.user" in q and "where u.username" in q:
            if not data:
                raise Exception("no data provided")
            if isinstance(data, dict):
                username = data.get("username")
            elif isinstance(data, (list, tuple)):
                username = data[2]
            else:
                username = data

            return {
                "id_user": 1,
                "user_type": "customer",
                "username": username,
                "password": "myHashedPassword",
                "sign_up_date": date.today(),
                "customer_name": "janjak",
                "customer_phone": "0000000000",
                "driver_name": None,
                "driver_phone": None,
                "vehicle_type": None,
                "availability": None,
                "admin_name": None,
                "admin_phone": None,
            }

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
