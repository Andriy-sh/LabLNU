from typing import Optional
from pydantic import BaseModel

class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryResponse(CategoryCreate):
    id: int
    
    class Config:
        orm_mode = True