from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class UserBase(SQLModel):
    first_name: str
    last_name: str
    email: str = Field(unique=True, index=True)
    password: str
    registration_date: datetime = Field(default_factory=datetime.utcnow)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    borrowed_books: List["BorrowedBook"] = Relationship(back_populates="user")