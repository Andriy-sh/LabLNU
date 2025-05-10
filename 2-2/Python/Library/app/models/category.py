from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from .associations import BookCategory

if TYPE_CHECKING:
    from .book import Book

class CategoryBase(SQLModel):
    name: str = Field(index=True)
    description: Optional[str] = None

class Category(CategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    books: List["Book"] = Relationship(
        back_populates="categories",
        link_model=BookCategory
    )