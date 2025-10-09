from src.DAO.userDAO import UserDAO  
from src.DAO.DBConnector import DBConnector
import logging

from dotenv import load_dotenv

load_dotenv()

# Configure le logging pour voir les erreurs
logging.basicConfig(level=logging.INFO)

# Initialise le connecteur à la base de données
db_connector = DBConnector()

# Crée une instance de UserDAO
userDAO = UserDAO(db_connector)

# Test de find_user_by_id
try:
    # Remplace 1 par un ID existant dans ta base
    user_dao = UserDAO(db_connector)   # ✅ Instanciation
    user = user_dao.find_user_by_id(1) # ✅ Appel sur l'instance


    if user is not None:
        print("✅ Utilisateur trouvé :")
        print(f"  - ID: {user.id_user}")
        print(f"  - Username: {user.username}")
  
    else:
        print("❌ Aucun utilisateur trouvé avec cet ID.")

except Exception as e:
    print(f"⚠️ Erreur lors de la récupération de l'utilisateur : {e}")


