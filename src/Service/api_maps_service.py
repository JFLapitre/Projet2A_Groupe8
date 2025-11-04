import urllib

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


address1 = address_dao.find_address_by_id(1)
print(address1)
# Exemple : on récupère une commande
order = order_dao.find_order_by_id(1)


origin: str = f"{order.address.street_number},{order.address.street_name}, {order.address.city}"

print(origin)


API_KEY = "AIzaSyBgOvV_du58_DMUTf7O8ACDt3SQ_USfeXE"

origin = "Rue des cerisiers,Longjumeau,France"
destination = "Bruz,France"
waypoints: list[str] = ["Marseille,France"]


url: str = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&waypoints={waypoints}&key={API_KEY}"

response = requests.get(url)
data = response.json()


# Exemple : afficher la distance et la durée
if data["status"] == "OK":
    route = data["routes"][0]
    legs = route.get("legs", [])
    maps_url = (
        "https://www.google.com/maps/dir/?api=1"
        f"&origin={urllib.parse.quote(origin)}"
        f"&destination={urllib.parse.quote(destination)}"
        f"&waypoints={'|'.join([urllib.parse.quote(w) for w in waypoints])}"
    )

    total_distance_m = sum(leg["distance"]["value"] for leg in legs)
    total_duration_s = sum(leg["duration"]["value"] for leg in legs)
    total_distance_km = total_distance_m / 1000  # km
    hours, remainder = divmod(total_duration_s, 3600)
    minutes, seconds = divmod(remainder, 60)

    print(f"Distance totale : {total_distance_km:.2f} km")
    print(f"Durée totale : {hours}h {minutes}min {seconds}s")
    print("Lien Google Maps :", maps_url)


else:
    print("Erreur :", data["status"])


class ApiMApsService:
    def __init__(self) -> None:
        self.user_dao = UserDAO()

    def Driveritinerary(destination, waypoints=[]):
        API_KEY = "AIzaSyBgOvV_du58_DMUTf7O8ACDt3SQ_USfeXE"
        origin = "51 Rue Blaise Pascal, Bruz, France"
        if waypoints != []:
            url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&waypoints={waypoints}&key={API_KEY}"

            response = requests.get(url)
            data = response.json()
            if data["status"] == "OK":
                route = data["routes"][0]
                legs = route.get("legs", [])
                maps_url = (
                    "https://www.google.com/maps/dir/?api=1"
                    f"&origin={urllib.parse.quote(origin)}"
                    f"&destination={urllib.parse.quote(destination)}"
                    f"&waypoints={'|'.join([urllib.parse.quote(w) for w in waypoints])}"
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

        else:
            url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={API_KEY}"

            response = requests.get(url)
            data = response.json()
            if data["status"] == "OK":
                route = data["routes"][0]
                legs = route.get("legs", [])
                maps_url = (
                    "https://www.google.com/maps/dir/?api=1"
                    f"&origin={urllib.parse.quote(origin)}"
                    f"&destination={urllib.parse.quote(destination)}"
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


Driveritinerary("18 Rue Charles Coudé, Bruz, France", waypoints=["17 Rue Jules lallemand, Rennes, France"])
