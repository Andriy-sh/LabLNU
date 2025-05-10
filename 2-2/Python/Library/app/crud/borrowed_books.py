from datetime import datetime
from typing import List
from sqlmodel import select
from app.crud.base import CRUDBase
from app.models.borrowed_book import BorrowedBook
from app.schemas.borrowed_book import BorrowedBookCreate, BorrowedBookResponse
from sqlmodel.ext.asyncio.session import Session

class CRUDBorrowedBook(CRUDBase[BorrowedBook, BorrowedBookCreate, BorrowedBookResponse]):
    def get_active_loans(self, db: Session) -> List[BorrowedBook]:
        return db.exec(
            select(BorrowedBook).where(BorrowedBook.returned_date == None)
        ).all()

    def return_book(self, db: Session, borrowed_book_id: int) -> BorrowedBook:
        borrowed_book = self.get(db, id=borrowed_book_id)
        if borrowed_book:
            borrowed_book.returned_date = datetime.utcnow()
            db.add(borrowed_book)
            db.commit()
            db.refresh(borrowed_book)
        return borrowed_book

borrowed_book = CRUDBorrowedBook(BorrowedBook)