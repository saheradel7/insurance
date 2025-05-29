import logging
from sqlalchemy.orm import Session

from .quote_model import Quote

from .quote_schema import QuoteCreate, QuoteRead
from fastapi import HTTPException, Depends
# from ..database import Database, get_db
from src.database import db_context
from sqlalchemy.orm import Session

# db = Database.get_instance().SessionLocal()


def create_quote(quote_in: QuoteCreate, agent_id: int, db: db_context) -> int:
    """
    Create a new quote row.
    Returns the new quote's .id on success.
    Raises CustomError on duplicate or other failures.
    """
    try:

        print("Quote to be inserted")
        quote = Quote(
            owner_id=agent_id,
            revision_number=quote_in.revision_number,
            revision_date=quote_in.revision_date,
            client_id=quote_in.client_id,
            property_id=quote_in.property_id,
            request_date=quote_in.request_date,
            status=quote_in.status,
            effective_date=quote_in.effective_date,
            expiration_date=quote_in.expiration_date,
            coverage_summary=quote_in.coverage_summary,
            estimated_risk_score=quote_in.estimated_risk_score,
            estimated_base_premium=quote_in.estimated_base_premium,
            expense_loading=quote_in.expense_loading,
            profit_margin=quote_in.profit_margin,
            contingency_loading=quote_in.contingency_loading,
            discounts=quote_in.discounts,
            final_estimated_premium=quote_in.final_estimated_premium,
            notes=quote_in.notes,
            last_modified_date=quote_in.last_modified_date,
            is_current=quote_in.is_current,
        )
        db.add(quote)
        print("inserting")
        db.commit()
        db.refresh(quote)
        print("Quote inserted successfully")
        return quote.id  # type: ignore

    except Exception as err:
        raise HTTPException(status_code=500, detail="Quote insert error: " + str(err))


def get_quote_by_id(quote_id: int, db: db_context) -> QuoteRead:
    """
    Fetch a User by its primary key.
    Raises CustomError if not found or other error happens.
    """
    try:
        quote = db.query(Quote).filter(Quote.id == quote_id).first()
        print("User fetched successfully")
        if not quote:
            raise HTTPException(status_code=404, detail="Quote not found.")
        return quote

    except Exception as err:
        print("Error in get_quote_by_id")
        raise HTTPException(status_code=500, detail="Quote fetch error: " + str(err))
