from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel


class CheckoutCreate(BaseModel):
    book_id: int
    patron_id: int


class CheckoutResponse(BaseModel):
    id: int
    book_id: int
    patron_id: int
    checkout_date: datetime
    due_date: datetime
    returned_date: Optional[datetime]

    class Config:
        orm_mode = True

