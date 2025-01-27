from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import  Session

from core.dependency import get_db
from schema.book_schema import BookCreate, BookResponse
from crud.book_crud import BookCRUD


router = APIRouter()

@router.post("/books/", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    try:
        book_crud = BookCRUD(db)
        return book_crud.create_book(book)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/books/", response_model=List[BookResponse])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        book_crud = BookCRUD(db)
        return book_crud.read_books(skip, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/books/{book_id}", response_model=BookResponse)
def read_book(book_id: int, db: Session = Depends(get_db)):
    try:
        book_crud = BookCRUD(db)
        return book_crud.read_book(book_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    try:
        book_crud = BookCRUD(db)
        return book_crud.update_book(book_id, book)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    try:
        book_crud = BookCRUD(db)
        return book_crud.delete_book(book_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))