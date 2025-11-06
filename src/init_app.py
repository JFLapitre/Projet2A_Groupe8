# src/init_app.py
from dotenv import load_dotenv

from src.DAO.DBConnector import DBConnector
from src.Service.address_service import AddressService
from src.Service.admin_menu_service import AdminMenuService
from src.Service.admin_user_service import AdminUserService
from src.Service.authentication_service import AuthenticationService
from src.Service.delivery_service import DeliveryService
from src.Service.driver_service import DriverService
from src.Service.JWTService import JwtService
from src.Service.order_service import OrderService
from src.Service.password_service import PasswordService

# Charger les variables d'environnement
load_dotenv()

# Connecteur DB
db_connector = DBConnector()

# Services
password_service = PasswordService()
auth_service = AuthenticationService(db_connector=db_connector, password_service=password_service)
item_service = AdminMenuService(db_connector=db_connector)
order_service = OrderService(db_connector=db_connector)
delivery_service = DeliveryService(db_connector=db_connector)
admin_user_service = AdminUserService(db_connector=db_connector)
jwt_service = JwtService()
address_service = AddressService(db_connector=db_connector)
driver_service = DriverService(db_connector=db_connector)
# Dictionnaire des services
services = {
    "auth": auth_service,
    "item": item_service,
    "order": order_service,
    "delivery": delivery_service,
    "user": admin_user_service,
    "jwt": jwt_service,
    "address": address_service,
    "driver": driver_service,
}
