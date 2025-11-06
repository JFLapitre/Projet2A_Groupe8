from dotenv import load_dotenv

from src.DAO.addressDAO import AddressDAO
from src.DAO.bundleDAO import BundleDAO
from src.DAO.DBConnector import DBConnector
from src.DAO.deliveryDAO import DeliveryDAO
from src.DAO.itemDAO import ItemDAO
from src.DAO.orderDAO import OrderDAO
from src.DAO.userDAO import UserDAO
from src.Service.admin_menu_service import AdminMenuService
from src.Service.admin_order_service import AdminOrderService
from src.Service.admin_user_service import AdminUserService
from src.Service.authentication_service import AuthenticationService
from src.Service.JWTService import JwtService
from src.Service.password_service import PasswordService

load_dotenv()

db_connector = DBConnector()
user_dao = UserDAO(db_connector=db_connector)
address_dao = AddressDAO(db_connector=db_connector)
item_dao = ItemDAO(db_connector=db_connector)
bundle_dao = BundleDAO(db_connector=db_connector, item_dao=item_dao)
order_dao = OrderDAO(
    db_connector=db_connector, user_dao=user_dao, address_dao=address_dao, bundle_dao=bundle_dao, item_dao=item_dao
)
delivery_dao = DeliveryDAO(db_connector=db_connector, user_dao=user_dao, order_dao=order_dao)

jwt_service = JwtService()
password_service = PasswordService()
auth_service = AuthenticationService(db_connector=db_connector, password_service=password_service)
admin_user_service = AdminUserService(db_connector=db_connector, password_service=password_service)
admin_order_service = AdminOrderService(delivery_dao=delivery_dao, order_dao=order_dao)
admin_menu_service = AdminMenuService(item_dao=item_dao, bundle_dao=bundle_dao)
