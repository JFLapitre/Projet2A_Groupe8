import urllib
import urllib.parse

import requests
from dotenv import load_dotenv

from src.DAO.addressDAO import AddressDAO
from src.DAO.bundleDAO import BundleDAO
from src.DAO.DBConnector import DBConnector
from src.DAO.deliveryDAO import DeliveryDAO
from src.DAO.itemDAO import ItemDAO
from src.DAO.orderDAO import OrderDAO
from src.DAO.userDAO import UserDAO


# Initialisations
db = DBConnector()
load_dotenv()
user_dao = UserDAO(db_connector=db)
address_dao = AddressDAO(db_connector=db)
item_dao = ItemDAO(db_connector=db)
bundle_dao = BundleDAO(db_connector=db, item_dao=item_dao)
order_dao = OrderDAO(db_connector=db, user_dao=user_dao, address_dao=address_dao, bundle_dao=bundle_dao)
delivery_dao = DeliveryDAO(db_connector=db, user_dao=user_dao, order_dao=order_dao)


class ApiMapsService:
    def __init__(self) -> None:
        self.delivery_dao = DeliveryDAO()

    def Driveritinerary(waypoints=[]):
        """
        Give an itinerary that starts and finishes at ENSAI and goes through all the waypoints.
        """
        API_KEY = "AIzaSyBgOvV_du58_DMUTf7O8ACDt3SQ_USfeXE"
        origin = "51 Rue Blaise Pascal, Bruz, France"
        destination = "51 Rue Blaise Pascal, Bruz, France"

        encoded_origin = urllib.parse.quote_plus(origin)
        encoded_destination = urllib.parse.quote_plus(destination)
        encoded_waypoints = "%7C".join(urllib.parse.quote_plus(w) for w in waypoints)

        url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&waypoints={waypoints}&key={API_KEY}"

        response = requests.get(url)
        data = response.json()
        if data["status"] == "OK":
            route = data["routes"][0]
            legs = route.get("legs", [])
            maps_url = (
                "https://www.google.com/maps/dir/?api=1"
                f"&origin={encoded_origin}"
                f"&destination={encoded_destination}"
                f"&waypoints={encoded_waypoints}"
            )
            total_distance_m = sum(leg["distance"]["value"] for leg in legs)
            total_duration_s = sum(leg["duration"]["value"] for leg in legs)
            total_distance_km = total_distance_m / 1000
            hours, remainder = divmod(total_duration_s, 3600)
            minutes, seconds = divmod(remainder, 60)

            print(f"Distance totale : {total_distance_km:.2f} km")
            print(f"Durée totale : {hours}h {minutes}min {seconds}s")
            print("Lien Google Maps :", maps_url)
        else:
            print("Erreur :", data["status"])

delivery = delivery_dao.find_delivery_by_id(1)

addresses = [
    f"{order.address.street_number} {order.address.street_name}, {order.address.city}, France"
    for order in delivery.orders

]
