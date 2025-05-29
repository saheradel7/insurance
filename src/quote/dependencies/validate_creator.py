from fastapi import HTTPException, Depends, Request
from typing import Annotated
from ..quote_schema import QuoteCreate
from ...auth.user_repository import get_user_by_keycloak_id
from ...dependencies.authentication_dependency import inject_dependencies_authentication
from ...auth.user_schema import UserRead
# from ...database import Database, get_db
from src.database import db_context, engine
from sqlalchemy.orm import Session


def validate_creator(
    request: Request,
    quote: QuoteCreate,
    keycloak_user_id: Annotated[str, Depends(inject_dependencies_authentication)],
    db: db_context,
    # user_to_create: Annotated[str, Depends(get_user_by_keycloak_id)],
) -> UserRead:
    print("Welcome")
    user_to_create = get_user_by_keycloak_id(keycloak_user_id, db)
    user_to_create_id = user_to_create.id
    print(user_to_create_id)
    print(quote.client_id)
    print(type(user_to_create_id))
    print(type(quote.client_id))
    if user_to_create_id == quote.client_id:
        raise HTTPException(
            status_code=400, detail="Can't create a quote for yourself!"
        )
    if user_to_create.role != "agent":
        raise HTTPException(status_code=403, detail="User is not an agent")
    print("Bye")
    return user_to_create
