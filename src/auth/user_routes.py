from fastapi import APIRouter
# from .user_controller import add_user
from .user_schema import UserCreate, UserRead
from fastapi import HTTPException, Depends
# from ..database import Database, get_db
from src.database import db_context, engine
from sqlalchemy.orm import Session
from .dependencies.keycloak import check_user_in_keycloak
import src.auth.user_model as user_model

# user_router = APIRouter(prefix="/insurance-users", tags=["insurance-users"])

# user_model.Base.metadata.create_all(bind=engine)

# @user_router.post("/", response_model=UserRead, status_code=201)
# async def create_user(
#     user: UserCreate,
#     db: db_context,
#     _: None = Depends(check_user_in_keycloak),
# ):
#     try:
#         return add_user(user, db)
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
