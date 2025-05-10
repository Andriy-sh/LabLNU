from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class BorrowedBookCreate(BaseModel):
    user_id: int
    book_id: int
    due_date: datetime

class BorrowedBookResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    borrowed_date: datetime
    due_date: datetime
    returned_date: Optional[datetime]
    
    class Config:
        orm_mode = True