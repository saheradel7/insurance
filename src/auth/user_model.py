# app/auth/models/users.py

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
# from ..database import Base
from src.database import Base
from typing import List


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # quote: Mapped[Quote] = relationship("Quote", back_populates="owner")
    # quotes: Mapped[List["Quote"]] = relationship(back_populates="owner")
    owned_quotes: Mapped[List["Quote"]] = relationship(
        "Quote",
        back_populates="owner",
        cascade="all, delete-orphan",
        foreign_keys="[Quote.owner_id]",
    )
    client_quotes: Mapped[List["Quote"]] = relationship(
        "Quote",
        back_populates="client",
        cascade="save-update, merge",  # ← *no* delete-orphan here
        foreign_keys="[Quote.client_id]",
    )
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    firstname: Mapped[str] = mapped_column(String)
    lastname: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String)
    keycloak_user_id: Mapped[str] = mapped_column(String)
