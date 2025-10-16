import logging
from typing import List, Optional, Union

from src.Model.abstract_user import AbstractUser
from src.Model.admin import Admin
from src.Model.customer import Customer
from src.Model.driver import Driver

from .DBConnector import DBConnector


class UserDAO:
    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector):
        self.db_connector = db_connector

    def find_user_by_id(self, id_user: int) -> Optional[Union[Customer, Driver, Admin]]:
        try:
            raw_user = self.db_connector.sql_query(
                """
                SELECT
                    u.*,
                    c.name as customer_name,
                    c.phone_number as customer_phone,
                    d.name as driver_name,
                    d.phone_number as driver_phone,
                    d.vehicle_type,
                    d.availability,
                    a.name as admin_name,
                    a.phone_number as admin_phone
                FROM fd.user u
                LEFT JOIN fd.customer c USING (id_user)
                LEFT JOIN fd.driver d USING (id_user)
                LEFT JOIN fd.admin a USING (id_user)
                WHERE u.id_user = %(id_user)s
                """,
                {"id_user": id_user},
                "one",
            )

            if not raw_user:
                return None

            user_type = raw_user["user_type"]
            if user_type == "customer":
                return Customer(
                    id_user=raw_user["id_user"],
                    username=raw_user["username"],
                    password=raw_user["password"],
                    sign_up_date=raw_user["sign_up_date"],
                    name=raw_user["customer_name"],
                    phone_number=raw_user["customer_phone"]
                )
            elif user_type == "driver":
                return Driver(
                    id_user=raw_user["id_user"],
                    username=raw_user["username"],
                    password=raw_user["password"],
                    sign_up_date=raw_user["sign_up_date"],
                    name=raw_user["driver_name"],
                    phone_number=raw_user["driver_phone"],
                    vehicle_type=raw_user["vehicle_type"],
                    availability=raw_user["availability"]
                )
            elif user_type == "admin":
                return Admin(
                    id_user=raw_user["id_user"],
                    username=raw_user["username"],
                    password=raw_user["password"],
                    sign_up_date=raw_user["sign_up_date"],
                    name=raw_user["admin_name"],
                    phone_number=raw_user["admin_phone"]
                )

        except Exception as e:
            logging.error(f"Failed to fetch user {id_user}: {e}")
            return None

    def find_user_by_username(self, username: int) -> Optional[Union[Customer, Driver, Admin]]:
        """Find a user by their username (returns the correct type)."""
        try:
            raw_user = self.db_connector.sql_query(
                """
                SELECT *
                FROM fd.user u
                LEFT JOIN fd.customer c USING (id_user)
                LEFT JOIN fd.driver d USING (id_user)
                LEFT JOIN fd.admin a USING (id_user)
                WHERE u.username = %(username)s
                """,
                {"username": username},
                "one",
            )
            if not raw_user:
                return None

            user_type = raw_user["user_type"]
            if user_type == "customer":
                return Customer(**raw_user)
            elif user_type == "driver":
                return Driver(**raw_user)
            elif user_type == "admin":
                return Admin(**raw_user)
        except Exception as e:
            logging.error(f"Failed to fetch user {username}: {e}")
            return None

    def find_all(self, user_type: Optional[str] = None) -> List[Union[Customer, Driver, Admin]]:
        """Find all users (optionally filtered by type)."""
        try:
            query = """
                SELECT *
                FROM fd.user u
                LEFT JOIN fd.customer c USING (id_user)
                LEFT JOIN fd.driver d USING (id_user)
                LEFT JOIN fd.admin a USING (id_user)
            """
            params = {}
            if user_type:
                query += " WHERE u.user_type = %(user_type)s"
                params["user_type"] = user_type

            raw_users = self.db_connector.sql_query(query, params, "all")
            users = []
            for user in raw_users:
                if user["user_type"] == "customer":
                    users.append(Customer(**user))
                elif user["user_type"] == "driver":
                    users.append(Driver(**user))
                elif user["user_type"] == "admin":
                    users.append(Admin(**user))
            return users
        except Exception as e:
            logging.error(f"Failed to fetch users: {e}")
            return []

    def add_user(self, user: Union[Customer, Driver, Admin]) -> Optional[Union[Customer, Driver, Admin]]:
        """Add a new user"""
        if isinstance(user, Customer):
            user_type = 'customer'
        elif isinstance(user, Driver):
            user_type = 'driver'
        elif isinstance(user, Admin):
            user_type = 'admin'

        result = self.db_connector.sql_query(
            """
        INSERT INTO fd.user (id_user, username, password, user_type)
        VALUES (DEFAULT, %(username)s, %(password)s, %(user_type)s)
        RETURNING id_user;
        """,
            {"username": user.username, "password": user.password, "user_type": user_type},
            "one",
        )
        id_user = result['id_user']
        if user_type == 'customer':
            self.db_connector.sql_query(
                """
                INSERT INTO fd.customer (id_user, name, phone_number)
                VALUES (%(id_user)s, %(name)s, %(phone_number)s)
                """,
                {"id_user": id_user, "name": user.name, "phone_number": user.phone_number},
                None
            )
        elif user_type == 'driver':
            self.db_connector.sql_query(
                """
                INSERT INTO fd.driver (id_user, name, phone_number, vehicle_type)
                VALUES (%(id_user)s, %(name)s, %(phone_number)s, %(vehicle_type)s)
                """,
                {
                    "id_user": id_user, 
                    "name": user.name,
                    "phone_number": user.phone_number, 
                    "vehicle_type": user.vehicle_type
                },
                None
            )
        elif user_type == 'admin':
            self.db_connector.sql_query(
                """
                INSERT INTO fd.admin (id_user, name, phone_number)
                VALUES (%(id_user)s, %(name)s, %(phone_number)s)
                """,
                {"id_user": id_user, "name": user.name, "phone_number": user.phone_number},
                None
            )

        # Retourne l'utilisateur complet
        return self.find_user_by_id(id_user)
