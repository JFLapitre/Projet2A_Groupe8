from src.DAO.DBConnector import DBConnector
from src.DAO.userDAO import UserDAO
from src.Model.customer import Customer
from src.Service.password_service import PasswordService


class AuthenticationService:
    def __init__(self, db_connector: DBConnector, password_service: PasswordService):
        """
        Secure authentication service.
        Injects UserDAO for data access and PasswordService for hashing/salting.
        """
        self.user_dao = UserDAO(db_connector=db_connector)
        self.password_service = password_service

    def login(self, username: str, password: str) -> Customer:
        """
        Authenticates a user (Customer) with username/password using manual salt verification.
        """
        user = self.user_dao.find_user_by_username(username)
        if not user:
            raise ValueError("User not found.")

        hashed_input_password = self.password_service.hash_password(password, user.salt)

        if hashed_input_password != user.hash_password:
            raise ValueError("Incorrect password.")

        return user

    def register(self, username: str, password: str, phone_number: str, user_type: str) -> Customer:
        """
        Registers a new user.
        The password is first checked for strength, then securely hashed and salted before storage.
        """
        if self.user_dao.find_user_by_username(username):
            raise ValueError(f"Username '{username}' already exists.")

        self.password_service.check_password_strength(password)

        salt = self.password_service.create_salt()

        hashed_password = self.password_service.hash_password(password, salt)

        new_user = self.user_dao.add_user_raw(
            username=username,
            password=hashed_password,
            phone_number=phone_number,
            user_type=user_type,
            salt=salt,
        )
        self.user_dao.add_user(new_user)

        return new_user
