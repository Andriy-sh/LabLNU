from typing import List
from sqlmodel import select
from app.crud.base import CRUDBase
from app.models.author import Author
from app.schemas.author import AuthorCreate, AuthorResponse
from sqlmodel.ext.asyncio.session import Session

class CRUDAuthor(CRUDBase[Author, AuthorCreate, AuthorResponse]):
    def get_by_name(self, db: Session, first_name: str, last_name: str) -> Author:
        return db.exec(
            select(Author)
            .where(Author.first_name == first_name)
            .where(Author.last_name == last_name)
        ).first()

author = CRUDAuthor(Author)