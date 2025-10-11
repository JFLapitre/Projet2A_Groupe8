import urllib

import requests

API_KEY = "AIzaSyBgOvV_du58_DMUTf7O8ACDt3SQ_USfeXE"

origin = "Longjumeau,France"
destination = "Bruz,France"
waypoints = ["Paris,France"]


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
