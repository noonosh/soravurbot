from datetime import datetime
from typing import Optional
from sqlalchemy import func
from sqlalchemy import BigInteger
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship
from .base import Base



class User(Base):
    
    __tablename__ = "users"
    
    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    username: Mapped[Optional[str]]
    email: Mapped[Optional[str]]
    language_code: Mapped[Optional[str]]
    added_date: Mapped[datetime] = mapped_column(insert_default=func.now())

    def __repr__(self) -> str:
        return f"User(id={self.user_id!r}, name={self.first_name!r})"


class Account(Base):
    
    __tablename__ = 'accounts'
    
    account_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'), primary_key=True)
    balance: Mapped[float] = mapped_column(default=0.00)
    