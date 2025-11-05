from fastapi import APIRouter, Depends, HTTPException, status

from .auth import admin_required
from .init_app import order_dao

order_router = APIRouter(prefix="/orders", tags=["Orders"], dependencies=[Depends(admin_required)])


@order_router.get("/{id_order}", status_code=status.HTTP_200_OK)
def find_order_by_id(id_order: int):
    try:
        my_order = order_dao.find_order_by_id(id_order)
        return my_order
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Movie with id [{}] not found".format(id_order),
        ) from FileNotFoundError
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid request") from Exception
