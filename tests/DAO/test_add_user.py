import logging
from datetime import datetime

from dotenv import load_dotenv

from src.DAO.DBConnector import DBConnector
from src.DAO.userDAO import UserDAO  # noqa: TID252
from src.Model.driver import Driver

load_dotenv()

# Configure le logging pour voir les erreurs
logging.basicConfig(level=logging.INFO)

# Initialise le connecteur à la base de données
db_connector = DBConnector()


# Crée une instance de UserDAO
userDAO = UserDAO(db_connector)
justinledriver = Driver(
    username="justincg",
    password="1234",
    name="Justinledriver",
    phone_number="0769522794",
    vehicle_type="bike",
    availability=True,
)


# Test de find_user_by_id
try:
    # Remplace 1 par un ID existant dans ta base
    user_dao = UserDAO(db_connector)  # ✅ Instanciation
    user = user_dao.add_user(justinledriver)  # ✅ Appel sur l'instance

    if user is not None:
        print("✅ Utilisateur trouvé :")
        print(f"  - ID: {user.id_user}")
        print(f"  - Username: {user.username}")

    else:
        print("❌ Aucun utilisateur trouvé avec cet ID.")

except Exception as e:
    print(f"⚠️ Erreur lors de la récupération de l'utilisateur : {e}")
