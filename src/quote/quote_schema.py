from pydantic import BaseModel
from datetime import date
from typing import Optional


class QuoteCreate(BaseModel):
    revision_number: int
    revision_date: date
    client_id: int
    property_id: int
    request_date: date
    status: str  # "under review", "approved", "rejected"
    effective_date: date
    expiration_date: date
    coverage_summary: Optional[str] = None
    estimated_risk_score: Optional[float] = None
    estimated_base_premium: Optional[float] = None
    expense_loading: Optional[float] = None
    profit_margin: Optional[float] = None
    contingency_loading: Optional[float] = None
    discounts: Optional[float] = None
    final_estimated_premium: Optional[float] = None
    notes: Optional[str] = None
    last_modified_date: Optional[date] = None
    is_current: Optional[bool] = None


class QuoteRead(BaseModel):
    id: int
    revision_number: int
    revision_date: date
    client_id: int
    owner_id: int
    property_id: int
    request_date: date
    status: str  # "under review", "approved", "rejected"
    effective_date: date
    expiration_date: date
    coverage_summary: Optional[str] = None
    estimated_risk_score: Optional[float] = None
    estimated_base_premium: Optional[float] = None
    expense_loading: Optional[float] = None
    profit_margin: Optional[float] = None
    contingency_loading: Optional[float] = None
    discounts: Optional[float] = None
    final_estimated_premium: Optional[float] = None
    notes: Optional[str] = None
    last_modified_date: Optional[date] = None
    is_current: Optional[bool] = None

    class Config:
        orm_mode = True
