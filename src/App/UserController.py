from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from src.Model.APIUser import APIUser

from .auth import admin_required
from .init_app import admin_user_service, jwt_service, password_service
from .JWTBearer import JWTBearer

if TYPE_CHECKING:
    from src.Model.User import User

user_router = APIRouter(prefix="/users", tags=["Users"])


def get_user_dao():
    return admin_user_service.user_dao


@user_router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(admin_required)])
def create_admin_user(username: str, password: str, name: str, phone_number: str) -> APIUser:
    """
    Performs validation on the username and password
    """
    try:
        password_service.check_password_strength(password=password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    try:
        user: User = admin_user_service.create_admin_account(
            username=username, password=password, name=name, phone_number=phone_number
        )

    except ValueError as error:
        raise HTTPException(status_code=409, detail=f"Conflict: {error}") from error

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    return APIUser(id_user=user.id_user, username=user.username)


@user_router.get("/me", dependencies=[Depends(JWTBearer())])
def get_user_own_profile(credentials: Annotated[HTTPAuthorizationCredentials, Depends(JWTBearer())]) -> APIUser:
    """
    Get the authenticated user profile
    """
    return get_user_from_credentials(credentials)


def get_user_from_credentials(credentials: HTTPAuthorizationCredentials, dao=Depends(get_user_dao)) -> APIUser:
    token = credentials.credentials
    id_user = int(jwt_service.validate_user_jwt(token))
    user: User | None = dao.find_user_by_id(id_user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return APIUser(id_user=user.id_user, username=user.username)


@user_router.post("/driver", status_code=status.HTTP_201_CREATED, dependencies=[Depends(admin_required)])
def create_driver_user(username: str, password: str, name: str, phone_number: str, vehicle_type: str) -> APIUser:
    """
    Performs validation and creates a new Driver account.
    This route requires an existing Admin to be authenticated.
    """
    try:
        password_service.check_password_strength(password=password)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    try:
        user: User = admin_user_service.create_driver_account(
            username=username,
            password=password,
            name=name,
            phone_number=phone_number,
            vehicle_type=vehicle_type,
        )

    except ValueError as error:
        raise HTTPException(status_code=409, detail=f"Conflict: {error}") from error

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    return APIUser(id_user=user.id_user, username=user.username)
