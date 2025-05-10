from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    publication_year: int
    isbn: str
    copies_available: int
    author_ids: List[int]
    category_ids: List[int]

class BookResponse(BaseModel):
    id: int
    title: str
    publication_year: int
    isbn: str
    copies_available: int

    class Config:
        orm_mode = True