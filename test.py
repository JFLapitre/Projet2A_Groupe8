from dotenv import load_dotenv

from src.DAO.DBConnector import DBConnector
from src.DAO.deliveryDAO import DeliveryDAO

load_dotenv()

dbconnector = DBConnector()
deliveryDAO = DeliveryDAO(dbconnector)

deliveries = deliveryDAO.find_all_deliveries()

for delivery in deliveries:
    print(delivery)