from dotenv import load_dotenv

from src.DAO.DBConnector import DBConnector

load_dotenv()


class ResetDatabaseTest:
    """
    Réinitialisation de la base de données en utilisant DBConnector et des fichiers SQL.
    """

    def lancer(self):
        print("Ré-initialisation de la base de données de test")

        try:
            with open("data/init_db_test.sql", encoding="utf-8") as init_db_test:
                init_db_test_as_string = init_db_test.read()

            with open("data/pop_db_test.sql", encoding="utf-8") as pop_db_test:
                pop_db_test_as_string = pop_db_test.read()

            db_connector = DBConnector()

            db_connector.sql_query(init_db_test_as_string, return_type=None)
            db_connector.sql_query(pop_db_test_as_string, return_type=None)

            print("Ré-initialisation de la base de données de test - Terminée")
            return True

        except FileNotFoundError as e:
            print(f"Erreur : Fichier SQL introuvable : {e}")
            raise
        except Exception as e:
            print(f"Erreur lors de la réinitialisation : {e}")
            raise


if __name__ == "__main__":
    ResetDatabaseTest().lancer()
