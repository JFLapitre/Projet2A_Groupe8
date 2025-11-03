from typing import List

from src.DAO.DBConnector import DBConnector
from src.DAO.userDAO import UserDAO
from src.Model.admin import Admin
from src.Model.customer import Customer
from src.Model.driver import Driver


class AdminUserService:
    def __init__(self, db_connector: DBConnector):
        """
        Initializes the service and injects dependencies into the UserDAO.
        """
        # UserDAO is the single DAO responsible for all user types
        self.user_dao = UserDAO(db_connector=db_connector)

    def create_admin_account(self, username: str, password: str, name: str, phone_number: str) -> Admin:
        """
        Validates and creates a new Admin account.
        'mail' from skeleton is used as 'username'. 'phone_number' is required by the DAO.
        """
        if not username or not password or not name:
            raise ValueError("Username, password, and name are required.")

        if self.user_dao.find_user_by_username(username):
            raise ValueError(f"Username '{username}' already exists.")

        # Assumes the Admin model can be instantiated without id or sign_up_date
        # The DAO's add_user handles those fields.
        new_admin = Admin(
            username=username,
            password=password,  # In a real app, hash this password
            name=name,
            phone_number=phone_number,
        )

        created_user = self.user_dao.add_user(new_admin)

        if not created_user or not isinstance(created_user, Admin):
            raise Exception("Failed to create admin account in the database.")

        return created_user

    def create_driver_account(
        self, username: str, password: str, name: str, phone_number: str, vehicle_type: str
    ) -> Driver:
        """
        Validates and creates a new Driver account.
        'mail' from skeleton is 'username'. 'phone_number' and 'vehicle_type' are required.
        """
        if not username or not password or not name:
            raise ValueError("Username, password, and name are required.")
        if not vehicle_type:
            raise ValueError("Vehicle type is required for a driver.")

        if self.user_dao.find_user_by_username(username):
            raise ValueError(f"Username '{username}' already exists.")

        # The DAO's add_user for drivers sets default availability
        new_driver = Driver(
            username=username,
            password=password,  # In a real app, hash this password
            name=name,
            phone_number=phone_number,
            vehicle_type=vehicle_type,
        )

        created_user = self.user_dao.add_user(new_driver)

        if not created_user or not isinstance(created_user, Driver):
            raise Exception("Failed to create driver account in the database.")

        return created_user

    def update_driver_availability(self, driver_id: int, availability: bool) -> Driver:
        """
        Updates a driver's availability status.
        """
        driver = self.user_dao.find_user_by_id(driver_id)
        if not driver or not isinstance(driver, Driver):
            raise ValueError(f"No valid driver found with ID {driver_id}")

        driver.availability = availability

        updated_driver = self.user_dao.update_user(driver)
        if not updated_driver or not isinstance(updated_driver, Driver):
            raise Exception("Failed to update driver availability.")

        return updated_driver

    def delete_user(self, user_id: int) -> bool:
        """
        Deletes any user (Admin, Driver, or Customer) by their ID.
        """
        user = self.user_dao.find_user_by_id(user_id)
        if not user:
            raise ValueError(f"No user found with ID {user_id}.")

        if not self.user_dao.delete_user(user_id):
            raise Exception(f"Failed to delete user {user_id}.")
        return True

    def list_all_users(self) -> List[Admin | Driver | Customer]:
        """
        Retrieves a list of all users from the database.
        """
        return self.user_dao.find_all()

    def list_drivers(self) -> List[Driver]:
        """
        Retrieves a list of all users with the 'driver' type.
        """
        return self.user_dao.find_all(user_type="driver")
