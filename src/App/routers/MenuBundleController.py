from typing import List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.App.auth import admin_required
from src.App.init_app import admin_menu_service
from src.Model.discounted_bundle import DiscountedBundle
from src.Model.one_item_bundle import OneItemBundle
from src.Model.predefined_bundle import PredefinedBundle

AnyBundle = Union[PredefinedBundle, DiscountedBundle, OneItemBundle]


menu_bundle_router = APIRouter(tags=["Menu Bundle management"], dependencies=[Depends(admin_required)])


def get_service():
    return admin_menu_service


def get_item_dao():
    return admin_menu_service.item_dao


def get_bundle_dao():
    return admin_menu_service.bundle_dao


def handle_service_error(e: Exception):
    msg = str(e).lower()
    if "not found" in msg:
        raise HTTPException(status_code=404, detail=str(e)) from e
    if isinstance(e, ValueError):
        raise HTTPException(status_code=400, detail=str(e)) from e
    print(f"Unexpected error: {e}")
    raise HTTPException(status_code=500, detail=str(e)) from e


@menu_bundle_router.get("/bundles/{id_bundle}", response_model=AnyBundle)
def get_bundle(id_bundle: int, dao=Depends(get_bundle_dao)):
    bundle = dao.find_bundle_by_id(id_bundle)
    if not bundle:
        raise HTTPException(status_code=404, detail=f"Bundle {id_bundle} not found")
    return bundle


@menu_bundle_router.get("/bundles", response_model=List[AnyBundle])
def list_bundles(service=Depends(get_service)):
    try:
        return service.list_bundles()
    except Exception as e:
        handle_service_error(e)


@menu_bundle_router.post("/bundles/predefined", status_code=status.HTTP_201_CREATED)
def create_predefined_bundle(
    name: str = Query(),
    price: float = Query(),
    availability: bool = Query(),
    item_ids: List[int] = Query(...),
    desc: Optional[str] = Query(None, alias="description"),
    service=Depends(get_service),
):
    try:
        service.create_predefined_bundle(
            name=name,
            description=desc,
            price=price,
            availability=availability,
            item_ids=item_ids,
        )
        return {"message": "Predefined bundle created"}
    except Exception as e:
        handle_service_error(e)


@menu_bundle_router.post("/bundles/discounted", status_code=status.HTTP_201_CREATED)
def create_discounted_bundle(
    name: str = Query(),
    required_item_types: List[str] = Query(),
    discount: float = Query(),
    desc: Optional[str] = Query(None, alias="description"),
    service=Depends(get_service),
):
    try:
        service.create_discounted_bundle(
            name=name,
            description=desc,
            discount=discount,
            required_item_types=required_item_types,
        )
        return {"message": "Predefined bundle created"}
    except Exception as e:
        handle_service_error(e)


@menu_bundle_router.delete("/bundles/{id_bundle}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bundle(id_bundle: int, service=Depends(get_service)):
    try:
        service.delete_bundle(id_bundle)
    except Exception as e:
        handle_service_error(e)
