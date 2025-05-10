from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    registration_date: datetime
    
    model_config = ConfigDict(from_attributes=True)