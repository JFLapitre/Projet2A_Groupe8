from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from src.DAO.addressDAO import AddressDAO
from src.DAO.bundleDAO import BundleDAO
from src.DAO.DBConnector import DBConnector
from src.DAO.itemDAO import ItemDAO
from src.DAO.orderDAO import OrderDAO
from src.DAO.userDAO import UserDAO
from src.Model.order import Order

order_router = APIRouter(prefix="/orders", tags=["Orders"])

@order_router.get("/{id_order}", status_code=status.HTTP_200_OK)
def find_order_by_id(id_order: int):
    try:
        my_order