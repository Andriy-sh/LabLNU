from typing import List
from sqlmodel import select
from app.crud.base import CRUDBase
from app.models.book import Book
from app.schemas.book import BookCreate, BookResponse
from sqlmodel.ext.asyncio.session import Session

class CRUDBook(CRUDBase[Book, BookCreate, BookResponse]):
    def get_by_isbn(self, db: Session, isbn: str) -> Book:
        return db.exec(select(Book).where(Book.isbn == isbn)).first()

    def get_by_author(self, db: Session, author_id: int) -> List[Book]:
        statement = select(Book).join(Book.authors).where(Author.id == author_id)
        return db.exec(statement).all()

    def get_by_category(self, db: Session, category_id: int) -> List[Book]:
        statement = select(Book).join(Book.categories).where(Category.id == category_id)
        return db.exec(statement).all()

book = CRUDBook(Book)