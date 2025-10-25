import logging

from dotenv import load_dotenv

from src.DAO.DBConnector import DBConnector
from src.DAO.userDAO import UserDAO

load_dotenv()

# Configure le logging pour voir les erreurs
logging.basicConfig(level=logging.INFO)

# Initialise le connecteur à la base de données
db_connector = DBConnector()

# Crée une instance de UserDAO
userDAO = UserDAO(db_connector)


try:
    user_dao = UserDAO(db_connector)
    users = user_dao.find_all()
    print(users is not None)
    if users is not None:
        print("✅ Utilisateurs trouvés :")
        for user in users:
            print(f"  - ID: {user.id_user}")
            print(f"  - Username: {user.username}")

    else:
        print("❌ Aucun utilisateur trouvé avec cet ID.")

except Exception as e:
    print(f"⚠️ Erreur lors de la récupération de l'utilisateur : {e}")
