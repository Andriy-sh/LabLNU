from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from .associations import BookAuthor, BookCategory

if TYPE_CHECKING:
    from .author import Author
    from .category import Category
    from .borrowed_book import BorrowedBook

class BookBase(SQLModel):
    title: str = Field(index=True)
    publication_year: int
    isbn: str = Field(unique=True)
    copies_available: int

class Book(BookBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    authors: List["Author"] = Relationship(
        back_populates="books",
        link_model=BookAuthor
    )
    categories: List["Category"] = Relationship(
        back_populates="books",
        link_model=BookCategory
    )
    borrowed_records: List["BorrowedBook"] = Relationship(back_populates="book")

    class Config:
        arbitrary_types_allowed = True