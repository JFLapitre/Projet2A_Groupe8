from typing import TYPE_CHECKING

from fastapi import APIRouter, HTTPException, status

from src.Model.JWTResponse import JWTResponse

from .init_app import auth_service, jwt_service

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
        raise 

    return jwt_service.encode_jwt(user.id_user)
