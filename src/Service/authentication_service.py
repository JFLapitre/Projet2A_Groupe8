import hashlib

from src.DAO.userDAO import UserDAO
from src.Model.customer import Customer


class AuthenticationService:
    def __init__(self, db_connector):
        """
        Service d'authentification utilisant la table user/customer
        """
        self.user_dao = UserDAO(db_connector=db_connector)

    def login(self, username: str, password: str) -> Customer:
        """
        Authentifie un utilisateur (customer) avec username/password
        """
        user = self.user_dao.find_user_by_username(username)
        if not user:
            raise ValueError("User not found")

        hashed_input = self._hash_function(password)
        if hashed_input != user.password:
            raise ValueError("Incorrect password")

        return user

    def register(self, username: str, password: str) -> Customer:
        if self.user_dao.find_user_by_username(username):
            raise ValueError(f"Username '{username}' already exists")

        hashed_password = self._hash_function(password)

        # Demande à la DAO de créer le user et de renvoyer un Customer complet avec id_user
        new_customer = self.user_dao.add_user_raw(
            username=username,
            password=hashed_password,
            phone_number="0000000000",
        )

        if not new_customer:
            raise Exception("Failed to create customer")

        return new_customer
