import logging
from datetime import date
from typing import List, Optional, Union

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
                    hash_password=raw_user["hash_password"],
                    salt=raw_user["salt"],
                    sign_up_date=raw_user["sign_up_date"],
                    name=raw_user["customer_name"],
                    phone_number=raw_user["customer_phone"],
                )
            elif user_type == "driver":
                return Driver(
                    id_user=raw_user["id_user"],
                    username=raw_user["username"],
                    hash_password=raw_user["hash_password"],
                    salt=raw_user["salt"],
                    sign_up_date=raw_user["sign_up_date"],
                    name=raw_user["driver_name"],
                    phone_number=raw_user["driver_phone"],
                    vehicle_type=raw_user["vehicle_type"],
                    availability=raw_user["availability"],
                )
            elif user_type == "admin":
                return Admin(
                    id_user=raw_user["id_user"],
                    username=raw_user["username"],
                    hash_password=raw_user["hash_password"],
                    salt=raw_user["salt"],
                    sign_up_date=raw_user["sign_up_date"],
                    name=raw_user["admin_name"],
                    phone_number=raw_user["admin_phone"],
                )

        except Exception as e:
            logging.error(f"Failed to fetch user {id_user}: {e}")
            return None

    def find_user_by_username(self, username: int) -> Optional[Union[Customer, Driver, Admin]]:
        """Find a user by their username (returns the correct type)."""
        try:
            raw_user = self.db_connector.sql_query(
                """
                SELECT u.*,
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
                SELECT u.*,
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
            """
            params = {}
            if user_type:
                query += " WHERE u.user_type = %(user_type)s"
                params["user_type"] = user_type

            raw_users = self.db_connector.sql_query(query, params, "all")
            users = []

            for user in raw_users:
                print(user)
                if user["user_type"] == "customer":
                    users.append(
                        Customer(
                            id_user=user["id_user"],
                            username=user["username"],
                            hash_password=user["hash_password"],
                            sign_up_date=user["sign_up_date"],
                            name=user["customer_name"],
                            phone_number=user["customer_phone"],
                            salt=user["salt"],
                        )
                    )
                elif user["user_type"] == "driver":
                    users.append(
                        Driver(
                            id_user=user["id_user"],
                            username=user["username"],
                            hash_password=user["hash_password"],
                            sign_up_date=user["sign_up_date"],
                            name=user["driver_name"],
                            phone_number=user["driver_phone"],
                            vehicle_type=user["vehicle_type"],
                            availability=user["availability"],
                            salt=user["salt"],
                        )
                    )
                elif user["user_type"] == "admin":
                    users.append(
                        Admin(
                            id_user=user["id_user"],
                            username=user["username"],
                            hash_password=user["hash_password"],
                            sign_up_date=user["sign_up_date"],
                            name=user["admin_name"],
                            phone_number=user["admin_phone"],
                            salt=user["salt"],
                        )
                    )
            print(users)
            return users
        except Exception as e:
            logging.error(f"Failed to fetch users: {e}")
            return []

    def add_user(self, user: Union[Customer, Driver, Admin]) -> Optional[Union[Customer, Driver, Admin]]:
        """Add a new user"""
        if isinstance(user, Customer):
            user_type = "customer"
        elif isinstance(user, Driver):
            user_type = "driver"
        elif isinstance(user, Admin):
            user_type = "admin"

        try:
            result = self.db_connector.sql_query(
                """
            INSERT INTO fd.user (id_user, username, hash_password, salt, user_type, sign_up_date)
            VALUES (DEFAULT, %(username)s, %(hash_password)s, %(salt)s, %(user_type)s, %(sign_up_date)s)
            RETURNING id_user;
            """,
                {
                    "username": user.username,
                    "hash_password": user.hash_password,
                    "salt": user.salt,
                    "user_type": user_type,
                    "sign_up_date": date.today(),
                },
                "one",
            )
            id_user = result["id_user"]

            if user_type == "customer":
                self.db_connector.sql_query(
                    """
                    INSERT INTO fd.customer (id_user, name, phone_number)
                    VALUES (%(id_user)s, %(name)s, %(phone_number)s)
                    """,
                    {"id_user": id_user, "name": user.name, "phone_number": user.phone_number},
                    None,
                )
            elif user_type == "driver":
                self.db_connector.sql_query(
                    """
                    INSERT INTO fd.driver (id_user, name, phone_number, vehicle_type, availability)
                    VALUES (%(id_user)s, %(name)s, %(phone_number)s, %(vehicle_type)s, %(availability)s)
                    """,
                    {
                        "id_user": id_user,
                        "name": user.name,
                        "phone_number": user.phone_number,
                        "vehicle_type": user.vehicle_type,
                        "availability": user.availability,
                    },
                    None,
                )
            elif user_type == "admin":
                self.db_connector.sql_query(
                    """
                    INSERT INTO fd.admin (id_user, name, phone_number)
                    VALUES (%(id_user)s, %(name)s, %(phone_number)s)
                    """,
                    {"id_user": id_user, "name": user.name, "phone_number": user.phone_number},
                    None,
                )

            return self.find_user_by_id(id_user)
        except Exception as e:
            logging.error(f"Failed to add user {user.username}: {e}")
            return None

    def update_user(self, user: Union[Customer, Driver, Admin]) -> Optional[Union[Customer, Driver, Admin]]:
        """Update an existing user"""
        try:
            if isinstance(user, Customer):
                user_type = "customer"
            elif isinstance(user, Driver):
                user_type = "driver"
            elif isinstance(user, Admin):
                user_type = "admin"

            self.db_connector.sql_query(
                """
                UPDATE fd.user
                SET username = %(username)s,
                    hash_password = %(hash_password)s,
                    user_type = %(user_type)s
                WHERE id_user = %(id_user)s
                """,
                {
                    "id_user": user.id_user,
                    "username": user.username,
                    "hash_password": user.hash_password,
                    "user_type": user_type,
                },
                None,
            )

            if user_type == "customer":
                self.db_connector.sql_query(
                    """
                    UPDATE fd.customer
                    SET name = %(name)s,
                        phone_number = %(phone_number)s
                    WHERE id_user = %(id_user)s
                    """,
                    {
                        "id_user": user.id_user,
                        "name": user.name,
                        "phone_number": user.phone_number,
                    },
                    None,
                )
            elif user_type == "driver":
                self.db_connector.sql_query(
                    """
                    UPDATE fd.driver
                    SET name = %(name)s,
                        phone_number = %(phone_number)s,
                        vehicle_type = %(vehicle_type)s,
                        availability = %(availability)s
                    WHERE id_user = %(id_user)s
                    """,
                    {
                        "id_user": user.id_user,
                        "name": user.name,
                        "phone_number": user.phone_number,
                        "vehicle_type": user.vehicle_type,
                        "availability": user.availability,
                    },
                    None,
                )
            elif user_type == "admin":
                self.db_connector.sql_query(
                    """
                    UPDATE fd.admin
                    SET name = %(name)s,
                        phone_number = %(phone_number)s
                    WHERE id_user = %(id_user)s
                    """,
                    {
                        "id_user": user.id_user,
                        "name": user.name,
                        "phone_number": user.phone_number,
                    },
                    None,
                )

            return self.find_user_by_id(user.id_user)
        except Exception as e:
            logging.error(f"Failed to update user {user.id_user}: {e}")
            return None

    def delete_user(self, id_user: int) -> bool:
        """Delete a user by ID"""
        try:
            user = self.find_user_by_id(id_user)
            if not user:
                logging.warning(f"User {id_user} not found, cannot delete")
                return False

            if isinstance(user, Customer):
                user_type = "customer"
            elif isinstance(user, Driver):
                user_type = "driver"
            elif isinstance(user, Admin):
                user_type = "admin"

            if user_type == "customer":
                self.db_connector.sql_query(
                    "DELETE FROM fd.customer WHERE id_user = %(id_user)s",
                    {"id_user": id_user},
                    None,
                )
            elif user_type == "driver":
                self.db_connector.sql_query(
                    "DELETE FROM fd.driver WHERE id_user = %(id_user)s",
                    {"id_user": id_user},
                    None,
                )
            elif user_type == "admin":
                self.db_connector.sql_query(
                    "DELETE FROM fd.admin WHERE id_user = %(id_user)s",
                    {"id_user": id_user},
                    None,
                )

            self.db_connector.sql_query(
                "DELETE FROM fd.user WHERE id_user = %(id_user)s",
                {"id_user": id_user},
                None,
            )

            return True
        except Exception as e:
            logging.error(f"Failed to delete user {id_user}: {e}")
            return False
