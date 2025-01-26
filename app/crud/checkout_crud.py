from datetime import datetime, timedelta
from http.client import HTTPException

from sqlalchemy import func

from models.book import Book
from models.checkout import Checkout
from models.patron import Patron
from schema.checkout_schema import CheckoutCreate


class CheckoutCRUD:
    def __init__(self, db):
        self.db = db

    def get_total_checkouts(self,start_date, end_date):
        return self.db.query(Checkout) \
            .filter(Checkout.checkout_date >= start_date) \
            .filter(Checkout.checkout_date <= end_date) \
            .count()

    def get_popular_books(self,start_date, end_date):
        return self.db.query(Book, func.count(Checkout.id).label('checkout_count')) \
            .join(Checkout) \
            .filter(Checkout.checkout_date >= start_date) \
            .filter(Checkout.checkout_date <= end_date) \
            .group_by(Book) \
            .order_by(func.count(Checkout.id).desc()) \
            .limit(5) \
            .all()

    def get_overdue_books(self):
        return  self.db.query(Checkout) \
            .filter(Checkout.returned_date.is_(None)) \
            .filter(Checkout.due_date < datetime.utcnow()) \
            .all()

    def checkout_book(self, checkout: CheckoutCreate):
        # Verify book exists and is available
        book = self.db.query(Book).filter(Book.id == checkout.book_id).first()
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        if not book.available:
            raise HTTPException(status_code=400, detail="Book is not available")

        # Verify patron exists
        patron = self.db.query(Patron).filter(Patron.id == checkout.patron_id).first()
        if patron is None:
            raise HTTPException(status_code=404, detail="Patron not found")

        # Create checkout record
        due_date = datetime.utcnow() + timedelta(days=14)  # 2-week checkout period
        db_checkout = Checkout(
            book_id=checkout.book_id,
            patron_id=checkout.patron_id,
            due_date=due_date
        )

        # Update book availability
        book.available = False

        self.db.add(db_checkout)
        self.db.commit()
        self.db.refresh(db_checkout)
        return db_checkout

    def get_checked_out_books(self):
        return self.db.query(Checkout).filter(Checkout.returned_date.is_(None)).all()

    def get_overdue_books(self):
        return self.db.query(Checkout) \
            .filter(Checkout.returned_date.is_(None)) \
            .filter(Checkout.due_date < datetime.utcnow()) \
            .all()

    def return_book(self, checkout_id: int):
        checkout = self.db.query(Checkout).filter(Checkout.id == checkout_id).first()
        if checkout is None:
            raise HTTPException(status_code=404, detail="Checkout record not found")
        if checkout.returned_date is not None:
            raise HTTPException(status_code=400, detail="Book already returned")

        # Update checkout record and book availability
        checkout.returned_date = datetime.utcnow()
        checkout.book.available = True

        self.db.commit()
        return {"message": "Book returned successfully"}