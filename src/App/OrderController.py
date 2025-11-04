from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from src.DAO.addressDAO import AddressDAO
from src.DAO.bundleDAO import BundleDAO
from src.DAO.DBConnector import DBConnector
from src.DAO.orderDAO import OrderDAO
from src.DAO.userDAO import UserDAO

db = DBConnector()
order_dao = OrderDAO(db, user_dao=UserDAO, address_dao=AddressDAO, bundle_dao=BundleDAO)

order_router = APIRouter(prefix="/orders", tags=["Orders"])


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
