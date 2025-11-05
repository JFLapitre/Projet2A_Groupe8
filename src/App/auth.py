from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from src.Model.abstract_user import AbstractUser
from src.Model.admin import Admin

from .init_app import jwt_service, user_dao
from .JWTBearer import JWTBearer


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())) -> AbstractUser:
    """
    Dépendance qui décode le token et retourne l'objet utilisateur complet
    (Admin, Customer, ou Driver) depuis la base de données.
    """
    try:
        token = credentials.credentials
        user_id = int(jwt_service.validate_user_jwt(token))

        user = user_dao.find_user_by_id(user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from e


def admin_required(current_user: AbstractUser = Depends(get_current_user)) -> Admin:
    """
    Dépendance qui vérifie que l'utilisateur authentifié est bien un Admin.
    Si ce n'est pas le cas, elle lève une erreur 403.
    """
    if not isinstance(current_user, Admin):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden: Admin rights required")
    return current_user
