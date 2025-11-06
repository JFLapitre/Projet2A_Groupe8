from typing import List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

# --- Imports des Modèles ---
from src.Model.abstract_bundle import AbstractBundle
from src.Model.discounted_bundle import DiscountedBundle
from src.Model.item import Item
from src.Model.one_item_bundle import OneItemBundle
from src.Model.predefined_bundle import PredefinedBundle

from .auth import admin_required
from .init_app import admin_menu_service, bundle_dao, item_dao

# --- Type Union pour les réponses polymorphiques ---
# On garde OneItemBundle ici au cas où il en existerait déjà en base et que list_bundles les renvoie.
AnyBundle = Union[PredefinedBundle, DiscountedBundle, OneItemBundle]

# =========================================
# DTOs (Modèles de Validation d'Entrée)
# =========================================


class ItemCreate(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    availability: bool = True
    item_type: str


class ItemUpdate(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    availability: bool
    item_type: str


class PredefinedBundleCreate(BaseModel):
    name: str
    description: str
    price: float
    availability: bool = True
    composition: List[int]  # Liste des IDs des items


class DiscountedBundleCreate(BaseModel):
    name: str
    description: str
    discount: float
    required_item_types: List[str]


# =========================================
# Contrôleur (MenuRouter)
# =========================================

menu_router = APIRouter(tags=["Admin Menu"], dependencies=[Depends(admin_required)])


# Dépendances
def get_service():
    return admin_menu_service


def get_bundle_dao():
    return bundle_dao


# Helper pour gérer les erreurs
def handle_service_error(e: Exception):
    msg = str(e).lower()
    if "not found" in msg:
        raise HTTPException(status_code=404, detail=str(e)) from e
    if isinstance(e, ValueError):
        raise HTTPException(status_code=400, detail=str(e)) from e
    print(f"Unexpected error: {e}")
    raise HTTPException(status_code=500, detail="Internal Server Error") from e


# =========================================
# Routes ITEMS
# =========================================


@menu_router.get("/items", response_model=List[Item])
def list_items(service=Depends(get_service)):
    try:
        return service.list_items()
    except Exception as e:
        handle_service_error(e)


@menu_router.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(
    name: str,
    price: float,
    stock: int,
    availability: bool,
    item_type: str,
    service=Depends(get_service),
    desc: str = None,
):
    try:
        service.create_item(
            name=name,
            desc=desc,
            price=price,
            stock=stock,
            availability=availability,
            item_type=item_type,
        )
        return {"message": "Item created successfully"}
    except Exception as e:
        handle_service_error(e)


@menu_router.put("/items/{item_id}")
def update_item(item_id: int, item_data: ItemUpdate, service=Depends(get_service)):
    try:
        service.update_item(
            id=item_id,
            name=item_data.name,
            desc=item_data.description,
            price=item_data.price,
            stock=item_data.stock,
            availability=item_data.availability,
            item_type=item_data.item_type,
        )
        return {"message": "Item updated successfully"}
    except Exception as e:
        handle_service_error(e)


@menu_router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, service=Depends(get_service)):
    try:
        service.delete_item(item_id)
    except Exception as e:
        handle_service_error(e)


# =========================================
# Routes BUNDLES
# =========================================


@menu_router.get("/bundles", response_model=List[AnyBundle])
def list_bundles(service=Depends(get_service)):
    try:
        return service.list_bundles()
    except Exception as e:
        handle_service_error(e)


@menu_router.get("/bundles/{bundle_id}", response_model=AnyBundle)
def get_bundle(bundle_id: int, dao=Depends(get_bundle_dao)):
    bundle = dao.find_bundle_by_id(bundle_id)
    if not bundle:
        raise HTTPException(status_code=404, detail=f"Bundle {bundle_id} not found")
    return bundle


@menu_router.delete("/bundles/{bundle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bundle(bundle_id: int, service=Depends(get_service)):
    try:
        service.delete_bundle(bundle_id)
    except Exception as e:
        handle_service_error(e)


@menu_router.post("/bundles/predefined", status_code=status.HTTP_201_CREATED)
def create_predefined_bundle(data: PredefinedBundleCreate, service=Depends(get_service)):
    try:
        service.create_predefined_bundle(
            name=data.name,
            description=data.description,
            composition=data.composition,
            availability=data.availability,
            price=data.price,
        )
        return {"message": "Predefined bundle created"}
    except Exception as e:
        handle_service_error(e)


@menu_router.post("/bundles/discounted", status_code=status.HTTP_201_CREATED)
def create_discounted_bundle(data: DiscountedBundleCreate, service=Depends(get_service)):
    try:
        service.create_discounted_bundle(
            name=data.name,
            description=data.description,
            required_item_types=data.required_item_types,
            discount=data.discount,
        )
        return {"message": "Discounted bundle created"}
    except Exception as e:
        handle_service_error(e)
