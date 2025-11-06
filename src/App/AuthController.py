from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from src.Model.APIUser import APIUser
from src.Model.JWTResponse import JWTResponse

from .auth import admin_required
from .init_app import admin_user_service, auth_service, jwt_service, password_service
from .JWTBearer import JWTBearer

if TYPE_CHECKING:
    from src.Model.User import User

auth_router = APIRouter(prefix="/auth", tags=["Authentification"])


@auth_router.post("/jwt", status_code=status.HTTP_201_CREATED)
def login(username: str, password: str) -> JWTResponse:
    """
    Authenticate with username and password and obtain a token
    """
    try:
        user = auth_service.login(username=username, password=password)
    except Exception as error:
        raise HTTPException(status_code=403, detail="Invalid username and password combination") from error

    return jwt_service.encode_jwt(user.id_user)
