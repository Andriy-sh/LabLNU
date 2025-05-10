from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from .associations import BookAuthor

class AuthorBase(SQLModel):
    first_name: str
    last_name: str
    biography: Optional[str] = None

class Author(AuthorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    books: List["Book"] = Relationship(
        back_populates="authors",
        link_model=BookAuthor
    )

    class Config:
        arbitrary_types_allowed = True