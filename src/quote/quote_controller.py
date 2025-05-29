from fastapi import HTTPException, Depends, Request, APIRouter

# from ..auth.user_model import User
from .quote_schema import QuoteCreate
from .quote_services import add_quote
from ..auth import user_repository
from sqlalchemy.orm import Session
from ..auth.user_schema import UserRead
from ..quote.quote_schema import QuoteRead
import src.quote.quote_model as quote_model
from .quote_routes import quote_router
from typing import Annotated
from .dependencies.validate_creator import validate_creator
from src.database import db_context, engine

quote_router = APIRouter(prefix="/quote", tags=["quote"])
print("hi quote")
quote_model.Base.metadata.create_all(bind=engine)


@quote_router.post("/", response_model=QuoteRead, status_code=201)
async def create_quote(
    quote: QuoteCreate,
    request: Request,
    user: Annotated[UserRead, Depends(validate_creator)],
    db: db_context,
    # keycloak_user_id: str = inject_dependencies_authentication,
):
    try:
        # keycloak_user_id = inject_dependencies_authentication(request)
        # print("creating quote")
        # return add_quote(quote, user, db)
        agent_id = user.id
        quote_instance = add_quote(quote, agent_id, db)
        return quote_instance
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# def add_quote(quote: QuoteCreate, user: UserRead, db: Session = Depends(get_db)):
#     try:
#         # Check if the agent exists in the database
#         # user = User.objects(keycloak_user_id=keycloak_user_id).first()
#         # user = user_repository.get_user_by_keycloak_id(keycloak_user_id, db)
#         # print("User:", user.firstname)
#         # if not user:
#         #     raise HTTPException(status_code=404, detail="User is not found")
#         # # Create a new quote
#         # if user.role != "agent":
#         #     raise HTTPException(status_code=403, detail="User is not an agent")
#         agent_id = user.id
#         quote_instance = create_quote(quote, agent_id, db)
#         return quote_instance
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
