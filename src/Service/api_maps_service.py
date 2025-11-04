import urllib

import requests
from dotenv import load_dotenv

from src.DAO.addressDAO import AddressDAO
from src.DAO.DBConnector import DBConnector
from src.DAO.orderDAO import OrderDAO

load_dotenv()
# Initialisation
db = DBConnector()
address_dao = AddressDAO(db_connector=db)
order_dao = OrderDAO(db_connector=db, address_dao=address_dao)

# Exemple : on récupère une commande
order = order_dao.find_order_by_id(1)

# Une seule ligne pour formater l’adresse d’origine :
origin = f"{order.address.street_number},{order.address.street_name}, {order.address.city}"

print(origin)


API_KEY = "AIzaSyBgOvV_du58_DMUTf7O8ACDt3SQ_USfeXE"

origin = "Rue des cerisiers,Longjumeau,France"
destination = "Bruz,France"
waypoints = ["Marseille,France"]


url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&waypoints={waypoints}&key={API_KEY}"

response = requests.get(url)
data = response.json()


# Exemple : afficher la distance et la durée
if data["status"] == "OK":
    route = data["routes"][0]
    leg = route["legs"][0]
    maps_url = (
        "https://www.google.com/maps/dir/?api=1"
        f"&origin={urllib.parse.quote(origin)}"
        f"&destination={urllib.parse.quote(destination)}"
        f"&waypoints={'|'.join([urllib.parse.quote(w) for w in waypoints])}"
    )
    print("Distance :", leg["distance"]["text"])
    print("Durée :", leg["duration"]["text"])
    print("Lien Google Maps :", maps_url)


else:
    print("Erreur :", data["status"])
