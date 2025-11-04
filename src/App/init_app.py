from dotenv import load_dotenv

from src.DAO.addressDAO import AddressDAO
from src.DAO.bundleDAO import BundleDAO
from src.DAO.DBConnector import DBConnector
from src.DAO.deliveryDAO import DeliveryDAO
from src.DAO.itemDAO import ItemDAO
from src.DAO.orderDAO import OrderDAO
from src.DAO.userDAO import UserDAO

# from src.Service.JWTService import JwtService

# from src.Service.UserService import UserService

load_dotenv()
db_connector = DBConnector()
user_dao = UserDAO(db_connector=db_connector)
address_dao = AddressDAO(db_connector=db_connector)
item_dao = ItemDAO(db_connector=db_connector)
bundle_dao = BundleDAO(db_connector=db_connector, item_dao=item_dao)
order_dao = OrderDAO(db_connector=db_connector, user_dao=user_dao, address_dao=address_dao, bundle_dao=bundle_dao)
delivery_dao = DeliveryDAO(db_connector=db_connector, user_dao=user_dao, order_dao=order_dao)

# jwt_service = JwtService()
# user_service = UserService(user_dao)
