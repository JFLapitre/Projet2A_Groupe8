from dotenv import load_dotenv

from src.DAO.addressDAO import AddressDAO
from src.DAO.bundleDAO import BundleDAO
from src.DAO.DBConnector import DBConnector
from src.DAO.deliveryDAO import DeliveryDAO
from src.DAO.itemDAO import ItemDAO
from src.DAO.orderDAO import OrderDAO
from src.DAO.userDAO import UserDAO

load_dotenv()

db_connector = DBConnector()
item_dao = ItemDAO(db_connector=db_connector)
user_dao = UserDAO(db_connector=db_connector)
address_dao = AddressDAO(db_connector=db_connector)
bundle_dao = BundleDAO(db_connector=db_connector, item_dao=item_dao)
order_dao = OrderDAO(db_connector=db_connector, user_dao=user_dao, address_dao=address_dao, bundle_dao=bundle_dao)
delivery_dao = DeliveryDAO(db_connector, user_dao, order_dao)

deliveries = delivery_dao.find_all_deliveries()

for delivery in deliveries:
    print(f"Livraison par {delivery.driver}")
    print(f"La livraison est {delivery.status}")
