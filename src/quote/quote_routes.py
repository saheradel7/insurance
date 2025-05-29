from fastapi import FastAPI, HTTPException, Request, APIRouter
# from .quote_controller import add_quote
from .quote_schema import QuoteCreate, QuoteRead
from ..dependencies.authentication_dependency import inject_dependencies_authentication
from fastapi import HTTPException, Depends
# from ..database import get_db
from sqlalchemy.orm import Session
from typing import Annotated
from .dependencies.validate_creator import validate_creator
from ..auth.user_schema import UserRead


quote_router = APIRouter(prefix="/quote", tags=["quote"])

# @quote_router.post("/", response_model=QuoteRead, status_code=201)
# async def create_quote(
#     quote: QuoteCreate,
#     request: Request,
#     user: Annotated[UserRead, Depends(validate_creator)],
#     db: Session = Depends(get_db),
#     # keycloak_user_id: str = inject_dependencies_authentication,
# ):
#     try:
#         # keycloak_user_id = inject_dependencies_authentication(request)
#         print("creating quote")
#         return add_quote(quote, user, db)
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
