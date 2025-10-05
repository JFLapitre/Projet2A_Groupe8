from dotenv import load_dotenv
from typing import Optional, Union, Literal
from psycopg2.extras import RealDictCursor

# Charge les variables d'environnement
load_dotenv()

class ResetDatabase:
    """
    Réinitialisation de la base de données en utilisant DBConnector et des fichiers SQL.
    """

    def lancer(self):
        print("Ré-initialisation de la base de données")

        try:
            # Lecture des fichiers SQL
            with open("data/init_db.sql", encoding="utf-8") as init_db:
                init_db_as_string = init_db.read()

            with open("data/pop_db.sql", encoding="utf-8") as pop_db:
                pop_db_as_string = pop_db.read()

            # Création du connecteur DB
            from src.DAO.DBConnector import DBConnector
            db_connector = DBConnector()

            # Exécution des scripts SQL en utilisant sql_query
            # Pour init_db.sql (création des tables)
            db_connector.sql_query(init_db_as_string, return_type = None)

            # Pour pop_db.sql (insertion des données)
            db_connector.sql_query(pop_db_as_string, return_type = None)

            print("Ré-initialisation de la base de données - Terminée")
            return True

        except FileNotFoundError as e:
            print(f"Erreur : Fichier SQL introuvable : {e}")
            raise
        except Exception as e:
            print(f"Erreur lors de la réinitialisation : {e}")
            raise

if __name__ == "__main__":
    ResetDatabase().lancer()
