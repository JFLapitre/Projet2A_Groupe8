from fastapi import APIRouter, HTTPException

from src.Model.order import Order  # À créer

order_router = APIRouter(prefix="/orders", tags=["Orders"])


@order_router.post("/", status_code=201)
def create_order(order: Order):
    """Permet à un client de passer une commande."""
    # Logique pour sauvegarder la commande en base de données
    return {"message": "Commande créée avec succès", "order_id": 123}


@order_router.get("/{order_id}")
def get_order(order_id: int):
    """Récupère les détails d'une commande."""
    # Logique pour récupérer la commande depuis la DB
    return {"order_id": order_id, "status": "en préparation"}
