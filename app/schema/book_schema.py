from datetime import datetime

from pydantic import BaseModel



# Pydantic Models
class BookBase(BaseModel):
    title: str
    author: str
    isbn: str


class BookCreate(BookBase):
    pass


class BookResponse(BookBase):
    id: int
    available: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


