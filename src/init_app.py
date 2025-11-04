# src/init_app.py
from dotenv import load_dotenv

from src.DAO.DBConnector import DBConnector
from src.Service.admin_menu_service import AdminMenuService
from src.Service.admin_user_service import AdminUserService

# Import de tous les services nécessaires
from src.Service.authentication_service import AuthenticationService
from src.Service.delivery_service import DeliveryService
from src.Service.JWTService import JwtService
from src.Service.order_service import OrderService

# Charger les variables d'environnement (.env)
load_dotenv()

# Initialisation du connecteur DB
db_connector = DBConnector()

# Services principaux
auth_service = AuthenticationService(db_connector)
item_service = AdminMenuService(db_connector)
order_service = OrderService(db_connector)
delivery_service = DeliveryService(db_connector)
admin_user_service = AdminUserService(db_connector)
jwt_service = JwtService()
