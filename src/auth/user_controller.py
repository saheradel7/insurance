from fastapi import HTTPException, Depends, APIRouter
# from ..database import get_db

from src.database import db_context, engine
from sqlalchemy.orm import Session
from .user_schema import UserCreate, UserRead, UserUpdate
from .user_services import create_user_service, get_user_by_id_service, get_user_by_keycloak_id_service, update_user_service, delete_user_service, get_all_users_service
import src.auth.user_model as user_model
from .dependencies.keycloak import check_user_in_keycloak




user_router = APIRouter(prefix="/insurance-users", tags=["insurance-users"])

user_model.Base.metadata.create_all(bind=engine)

@user_router.post("/", response_model=UserRead, status_code=201)
async def create_user(
    user: UserCreate,
    db: db_context,
    _: None = Depends(check_user_in_keycloak),
):
    try:
        return create_user_service(user, db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@user_router.get("/", response_model=list[UserRead], status_code=200)
async def get_users(
    db: db_context,
):
    """
    Get all users
    """
    try:
        return get_all_users_service(db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))   


@user_router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    db: db_context,
):
    """
    Get a user by ID.
    """
    try:
        user = get_user_by_id_service(user_id, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@user_router.get("/by-keycloak-id/{user_keycloak_id}", response_model=UserRead)
async def get_user(
    user_keycloak_id: str,
    db: db_context,
):
    """
    Get a user by ID.
    """
    try:
        user = get_user_by_keycloak_id_service(user_keycloak_id, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@user_router.put("/{user_keycloak_id}", response_model=UserRead)
async def update_user(
    user_keycloak_id: str,
    user: UserUpdate,
    db: db_context,
):
    """
    Update a user by keycloak ID.
    """
    try:
        return update_user_service(user_keycloak_id, user, db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_router.delete("/{user_keycloak_id}")
async def delete_user(
    user_keycloak_id: str,
    db: db_context,
):
    """
    Update a user by keycloak ID.
    """
    try:
        return delete_user_service(user_keycloak_id, db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    
    
