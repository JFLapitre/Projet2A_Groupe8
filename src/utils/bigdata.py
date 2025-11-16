from dotenv import load_dotenv
from faker import Faker

from src.DAO.DBConnector import DBConnector

from .bulk import generate_bulk_items, generate_discounted_bundles, generate_predefined_bundles

load_dotenv()


class ResetDatabase:
    """
    Resetting the database using DBConnector and SQL files.
    """

    def __init__(self):
        self.fake = Faker("fr_FR")
        self.db_connector = DBConnector()


    def lancer(self):
        print("Database reset")

        try:
            with open("data/init_db.sql", encoding="utf-8") as init_db:
                init_db_as_string = init_db.read()

            with open("data/pop_db.sql", encoding="utf-8") as pop_db:
                pop_db_as_string = pop_db.read()

            self.db_connector.sql_query(init_db_as_string, return_type=None)
            self.db_connector.sql_query(pop_db_as_string, return_type=None)

            generate_bulk_items(self.db_connector, item_count=5000)
            generate_discounted_bundles(self.db_connector)
            generate_predefined_bundles(self.db_connector)

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
