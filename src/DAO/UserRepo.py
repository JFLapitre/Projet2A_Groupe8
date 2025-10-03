from typing import Optional

from src.Model.User import User

from .DBConnector import DBConnector


class UserDAO:
    db_connector: DBConnector

    def __init__(self, db_connector: DBConnector):
        self.db_connector = db_connector

    def find_user_by_id(self, user_id: int) -> Optional[User]:
        raw_user = self.db_connector.sql_query("SELECT * from user WHERE id=%s", [user_id], "one")
        if raw_user is None:
            return None
        return User(**raw_user)

    def find_user_by_username(self, username: str) -> Optional[User]:
        raw_user = self.db_connector.sql_query("SELECT * from user WHERE username=%s", [username], "one")
        if raw_user is None:
            return None
        # pyrefly: ignore
        return User(**raw_user)

    def add_user(self, username: str, salt: str, hashed_password: str) -> User:
        raw_created_user = self.db_connector.sql_query(
            """
        INSERT INTO user (id, username, salt, password)
        VALUES (DEFAULT, %(username)s, %(salt)s, %(password)s)
        RETURNING *;
        """,
            {"username": username, "salt": salt, "password": hashed_password},
            "one",
        )
        # pyrefly: ignore
        return User(**raw_created_user)
