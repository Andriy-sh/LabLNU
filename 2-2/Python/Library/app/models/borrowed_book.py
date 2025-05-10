from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class BorrowedBookBase(SQLModel):
    borrowed_date: datetime = Field(default_factory=datetime.utcnow)
    due_date: datetime
    returned_date: Optional[datetime] = None

class BorrowedBook(BorrowedBookBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    book_id: int = Field(foreign_key="book.id")
    
    user: "User" = Relationship(back_populates="borrowed_books")
    book: "Book" = Relationship(back_populates="borrowed_records")