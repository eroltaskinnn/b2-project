from datetime import datetime, timedelta
from sqlalchemy import  Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from core.database import Base
from .common import CommonModel


class Checkout(CommonModel):
    __tablename__ = "checkouts"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    patron_id = Column(Integer, ForeignKey("patrons.id"))
    checkout_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime)
    returned_date = Column(DateTime, nullable=True)

    book = relationship("Book", back_populates="checkouts")
    patron = relationship("Patron", back_populates="checkouts")


# metadata = Base.metadata

