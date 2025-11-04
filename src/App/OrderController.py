from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
from pydantic import BaseModel

from src.Model.order import Order
from src.DAO.orderDAO import OrderDAO
from src.DAO.userDAO import UserDAO
from src.DAO.addressDAO import AddressDAO
from src.DAO.bundleDAO import BundleDAO
from src.DAO.itemDAO import ItemDAO
from src.DAO.DBConnector import DBConnector

order_router = APIRouter(prefix="/orders", tags=["Orders"])


# Dependency pour obtenir les DAOs
def get_order_dao() -> OrderDAO:
    """Dependency injection pour OrderDAO."""
    db_connector = DBConnector()
    user_dao = UserDAO(db_connector=db_connector)
    address_dao = AddressDAO(db_connector=db_connector)
    item_dao = ItemDAO(db_connector=db_connector)
    bundle_dao = BundleDAO(db_connector=db_connector, item_dao=item_dao)
    return OrderDAO(
        db_connector=db_connector,
        user_dao=user_dao,
        address_dao=address_dao,
        bundle_dao=bundle_dao
    )


# Schéma pour créer une commande (sans id_order)
class OrderCreate(BaseModel):
    id_user: int
    id_address: int
    bundle_ids: List[int]  # Liste des IDs de bundles
    status: str = "pending"


# Schéma pour mettre à jour une commande
class OrderUpdate(BaseModel):
    id_user: Optional[int] = None
    id_address: Optional[int] = None
    bundle_ids: Optional[List[int]] = None
    status: Optional[str] = None


@order_router.post("/", status_code=status.HTTP_201_CREATED)
def create_order(order_data: OrderCreate, order_dao: OrderDAO = Depends(get_order_dao)):
    """Permet à un client de passer une commande."""
    try:
        # Récupère le customer
        customer = order_dao.user_dao.find_user_by_id(order_data.id_user)
        if not customer:
            raise HTTPException(status_code=404, detail=f"Customer with id {order_data.id_user} not found")
        
        # Récupère l'adresse
        address = order_dao.address_dao.find_address_by_id(order_data.id_address)
        if not address:
            raise HTTPException(status_code=404, detail=f"Address with id {order_data.id_address} not found")
        
        # Récupère les bundles
        bundles = []
        for bundle_id in order_data.bundle_ids:
            bundle = order_dao.bundle_dao.find_bundle_by_id(bundle_id)
            if not bundle:
                raise HTTPException(status_code=404, detail=f"Bundle with id {bundle_id} not found")
            bundles.append(bundle)
        
        # Crée l'objet Order
        from datetime import datetime
        new_order = Order(
            id_order=0,  # Sera généré par la DB
            customer=customer,
            address=address,
            bundles=bundles,
            status=order_data.status,
            order_date=datetime.now()
        )
        
        # Sauvegarde en base
        created_order = order_dao.add_order(new_order)
        
        if not created_order:
            raise HTTPException(status_code=500, detail="Failed to create order")
        
        return {
            "message": "Commande créée avec succès",
            "order_id": created_order.id_order,
            "order": created_order
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@order_router.get("/{order_id}", response_model=Order)
def get_order(order_id: int, order_dao: OrderDAO = Depends(get_order_dao)):
    """Récupère les détails d'une commande."""
    order = order_dao.find_order_by_id(order_id)
    
    if not order:
        raise HTTPException(status_code=404, detail=f"Order with id {order_id} not found")
    
    return order


@order_router.get("/", response_model=List[Order])
def get_all_orders(order_dao: OrderDAO = Depends(get_order_dao)):
    """Récupère toutes les commandes."""
    orders = order_dao.find_all_orders()
    return orders


@order_router.get("/customer/{customer_id}", response_model=List[Order])
def get_orders_by_customer(customer_id: int, order_dao: OrderDAO = Depends(get_order_dao)):
    """Récupère toutes les commandes d'un client spécifique."""
    # Vérifie que le customer existe
    customer = order_dao.user_dao.find_user_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer with id {customer_id} not found")
    
    orders = order_dao.find_orders_by_customer(customer_id)
    return orders


@order_router.put("/{order_id}")
def update_order(
    order_id: int,
    order_update: OrderUpdate,
    order_dao: OrderDAO = Depends(get_order_dao)
):
    """Met à jour une commande existante."""
    # Récupère la commande existante
    existing_order = order_dao.find_order_by_id(order_id)
    if not existing_order:
        raise HTTPException(status_code=404, detail=f"Order with id {order_id} not found")
    
    try:
        # Met à jour les champs fournis
        if order_update.id_user is not None:
            customer = order_dao.user_dao.find_user_by_id(order_update.id_user)
            if not customer:
                raise HTTPException(status_code=404, detail=f"Customer with id {order_update.id_user} not found")
            existing_order.customer = customer
        
        if order_update.id_address is not None:
            address = order_dao.address_dao.find_address_by_id(order_update.id_address)
            if not address:
                raise HTTPException(status_code=404, detail=f"Address with id {order_update.id_address} not found")
            existing_order.address = address
        
        if order_update.bundle_ids is not None:
            bundles = []
            for bundle_id in order_update.bundle_ids:
                bundle = order_dao.bundle_dao.find_bundle_by_id(bundle_id)
                if not bundle:
                    raise HTTPException(status_code=404, detail=f"Bundle with id {bundle_id} not found")
                bundles.append(bundle)
            existing_order.bundles = bundles
        
        if order_update.status is not None:
            existing_order.status = order_update.status
        
        # Sauvegarde les modifications
        success = order_dao.update_order(existing_order)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update order")
        
        # Récupère la commande mise à jour
        updated_order = order_dao.find_order_by_id(order_id)
        
        return {
            "message": "Commande mise à jour avec succès",
            "order": updated_order
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@order_router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, order_dao: OrderDAO = Depends(get_order_dao)):
    """Supprime une commande."""
    # Vérifie que la commande existe
    order = order_dao.find_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order with id {order_id} not found")
    
    success = order_dao.delete_order(order_id)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete order")
    
    return None  # 204 No Content ne retourne rien


@order_router.patch("/{order_id}/status")
def update_order_status(
    order_id: int,
    new_status: str,
    order_dao: OrderDAO = Depends(get_order_dao)
):
    """Met à jour uniquement le statut d'une commande."""
    # Récupère la commande existante
    existing_order = order_dao.find_order_by_id(order_id)
    if not existing_order:
        raise HTTPException(status_code=404, detail=f"Order with id {order_id} not found")
    
    # Valide le statut
    valid_statuses = ["pending", "in_progress", "delivered", "cancelled"]
    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )
    
    existing_order.status = new_status
    success = order_dao.update_order(existing_order)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update order status")
    
    updated_order = order_dao.find_order_by_id(order_id)
    
    return {
        "message": f"Statut de la commande mis à jour à '{new_status}'",
        "order": updated_order
    }