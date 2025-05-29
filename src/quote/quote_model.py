# app/quote/quote_model.py

from datetime import date
from sqlalchemy import Integer, String, Date, Float, ForeignKey, UniqueConstraint, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

# from ..database import Base
from src.database import Base


class Quote(Base):
    __tablename__ = "quotes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    revision_number: Mapped[int] = mapped_column(Integer)
    revision_date: Mapped[date] = mapped_column(Date)
    # client_id: Mapped[str] = mapped_column(String)

    owner_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),  # optional DB-level cascade,
        nullable=False,
    )
    # Explicitly refer to the User class name
    owner: Mapped["User"] = relationship(
        "User",
        back_populates="owned_quotes",
        foreign_keys=[owner_id],
        passive_deletes=True,  # relies on DB ON DELETE CASCADE
    )
    client_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    client: Mapped["User"] = relationship(
        "User", back_populates="client_quotes", foreign_keys=[client_id]
    )
    property_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("properties.id", ondelete="CASCADE"),
        nullable=False,
    )
    property: Mapped["Property"] = relationship(
        "Property",
        back_populates="quotes",
        # passive_deletes=True,
    )

    # property_id: Mapped[int] = mapped_column(Integer)
    request_date: Mapped[date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(
        String
    )  # "under review", "approved", "rejected"
    effective_date: Mapped[date] = mapped_column(Date)
    expiration_date: Mapped[date] = mapped_column(Date)
    coverage_summary: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )
    estimated_risk_score: Mapped[Optional[Float]] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )
    estimated_base_premium: Mapped[Optional[Float]] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )
    expense_loading: Mapped[Optional[Float]] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )
    profit_margin: Mapped[Optional[Float]] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )
    contingency_loading: Mapped[Optional[Float]] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )
    discounts: Mapped[Optional[Float]] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )
    final_estimated_premium: Mapped[Optional[Float]] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )
    notes: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )
    last_modified_date: Mapped[Optional[Date]] = mapped_column(
        Date,
        nullable=True,
    )
    is_current: Mapped[Optional[bool]] = mapped_column(
        Integer,
        nullable=True,
    )
    
    # enforce one-quote per client per property
    __table_args__ = (
        UniqueConstraint("client_id", "property_id", name="uq_client_property"),
    )
