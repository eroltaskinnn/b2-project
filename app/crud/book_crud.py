from sqlalchemy.orm import Session
from models.book import Book
from schema.book_schema import BookCreate, BookResponse
from fastapi import HTTPException


class BookCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create_book(self, book: BookCreate):
        db_book = Book(**book.dict())
        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)
        return db_book

    def read_books(self, skip: int = 0, limit: int = 100):
        return self.db.query(Book).offset(skip).limit(limit).all()

    def read_book(self, book_id: int):
        book = self.db.query(Book).filter(Book.id == book_id).first()
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        return book

    def update_book(self, book_id: int, book: BookCreate):
        db_book = self.db.query(Book).filter(Book.id == book_id).first()
        if db_book is None:
            raise HTTPException(status_code=404, detail="Book not found")

        for key, value in book.dict().items():
            setattr(db_book, key, value)

        self.db.commit()
        self.db.refresh(db_book)
        return db_book

    def delete_book(self, book_id: int):
        book = self.db.query(Book).filter(Book.id == book_id).first()
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")

        self.db.delete(book)
        self.db.commit()
        return {"message": "Book deleted successfully"}