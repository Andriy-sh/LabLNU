from typing import Optional
from pydantic import BaseModel

class AuthorCreate(BaseModel):
    first_name: str
    last_name: str
    biography: Optional[str] = None

class AuthorResponse(AuthorCreate):
    id: int
    
    class Config:
        orm_mode = True