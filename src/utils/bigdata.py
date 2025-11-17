import random

from dotenv import load_dotenv
from faker import Faker

from src.DAO.DBConnector import DBConnector
from src.Service.password_service import PasswordService

load_dotenv()


class ResetDatabase:
    """
    Resetting the database using DBConnector and SQL files and add 10 000 fake users.
    """

    def __init__(self):
        self.fake = Faker("fr_FR")
        self.db_connector = DBConnector()
        self.service = PasswordService()
        self.fake = Faker()

    def generate_bulk_users(self, user_count=10000):
        next_id = 14
        user_sql_values = []
        customer_sql_values = []
        admin_sql_values = []
        driver_sql_values = []

        user_types = ["customer", "admin", "driver"]
        vehicle_types = ["car", "bike"]

        for i in range(user_count):
            id_user = next_id + i

            name = self.fake.name().replace("'", "''")
            username = self.fake.user_name().replace("'", "''")
            phone_number = self.fake.phone_number()
            password = self.fake.password()
            salt = self.service.create_salt()
            hashed_password = self.service.hash_password(password, salt)
            user_type = random.choice(user_types)
            sign_up_date = self.fake.date()

            safe_username = username.replace("'", "''")

            user_sql_values.append(
                f"({id_user}, '{safe_username}', '{hashed_password}', '{salt}', '{user_type}', '{sign_up_date}')"
            )
            if user_type == "customer":
                customer_sql_values.append(f"({id_user}, '{name}', '{phone_number}')")

            elif user_type == "admin":
                admin_sql_values.append(f"({id_user}, '{name}', '{phone_number}')")

            elif user_type == "driver":
                vehicle = random.choice(vehicle_types)
                availability = random.choice(["TRUE", "FALSE"])
                driver_sql_values.append(f"({id_user}, '{name}', '{phone_number}', '{vehicle}', {availability})")

        full_query_user = (
            "INSERT INTO fd.user (id_user, username, hash_password, salt, user_type, sign_up_date) VALUES "
        )
        full_query_user += ", ".join(user_sql_values) + ";"

        full_query_customer = "INSERT INTO fd.customer (id_user, name, phone_number) VALUES "
        full_query_customer += ", ".join(customer_sql_values) + ";"

        full_query_admin = "INSERT INTO fd.admin (id_user, name, phone_number) VALUES "
        full_query_admin += ", ".join(admin_sql_values) + ";"

        full_query_driver = "INSERT INTO fd.driver (id_user, name, phone_number, vehicle_type, availability) VALUES "
        full_query_driver += ", ".join(driver_sql_values) + ";"

        try:
            self.db_connector.sql_query(full_query_user, return_type=None)
            print(f"{user_count} users successfully added.")

            self.db_connector.sql_query(full_query_customer, return_type=None)
            print(f"{len(customer_sql_values)} clients ajoutés.")

            self.db_connector.sql_query(full_query_admin, return_type=None)
            print(f"{len(admin_sql_values)} admins ajoutés.")

            self.db_connector.sql_query(full_query_driver, return_type=None)
            print(f"{len(driver_sql_values)} chauffeurs ajoutés.")

        except Exception as e:
            print(f"Erreur lors de l'insertion de masse des users : {e}")
            raise

    def lancer(self):
        print("Database reset")

        try:
            with open("data/init_db.sql", encoding="utf-8") as init_db:
                init_db_as_string = init_db.read()

            with open("data/pop_db.sql", encoding="utf-8") as pop_db:
                pop_db_as_string = pop_db.read()

            self.db_connector.sql_query(init_db_as_string, return_type=None)
            self.db_connector.sql_query(pop_db_as_string, return_type=None)

            self.generate_bulk_users()

            print("Database reset - Complete")
            return True

        except FileNotFoundError as e:
            print(f"Error: SQL file not found : {e}")
            raise
        except Exception as e:
            print(f"Error during reset : {e}")
            raise


if __name__ == "__main__":
    ResetDatabase().lancer()
