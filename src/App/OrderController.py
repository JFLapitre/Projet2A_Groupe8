from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from src.Model.order import Order

from .auth import admin_required
from .init_app import admin_order_service

order_router = APIRouter(prefix="/orders", tags=["Consulting orders"], dependencies=[Depends(admin_required)])

def get_admin_order_service():
    return admin_order_service

def get_order_dao():
    return admin_order_service.order_dao

@order_router.get("/{id_order}", status_code=status.HTTP_200_OK)
def find_order_by_id(id_order: int, dao = Depends(get_order_dao)):
    try:
        my_order = dao.find_order_by_id(id_order)
        return my_order
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Movie with id [{}] not found".format(id_order),
        ) from FileNotFoundError
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid request") from Exception


@order_router.get("/", status_code=status.HTTP_200_OK, response_model=List[Order])
def get_pending_orders(admin_service = Depends(get_admin_order_service)):
    """
    Retrieves all orders with the status 'pending'.
    This route is protected and accessible only to administrators.
    """
    try:
        pending_orders = admin_service.list_waiting_orders()
        return pending_orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching orders: {e}") from e
