import logging
from typing import Any
from fastapi import HTTPException, Depends
from .quote_schema import QuoteCreate, QuoteRead
from . import quote_reprository
# from ..database import Database, get_db
from src.database import db_context
from sqlalchemy.orm import Session


def add_quote(quote: QuoteCreate, agent_id: int, db: db_context) -> QuoteRead:
    """
    Create a new quote via the repository, then fetch and return it.
    """
    try:
        # Create the quote and get its new ID
        quote_id = quote_reprository.create_quote(quote, agent_id, db)
        print("User ID:", quote_id)
        return quote_reprository.get_quote_by_id(quote_id, db)

    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail="An error occurred while creating the quote.",
        )
