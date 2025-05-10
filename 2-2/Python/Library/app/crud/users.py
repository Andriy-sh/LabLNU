from typing import List
from sqlmodel import select
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from sqlmodel.ext.asyncio.session import Session

class CRUDUser(CRUDBase[User, UserCreate, UserResponse]):
    def get_by_email(self, db: Session, email: str) -> User:
        return db.exec(select(User).where(User.email == email)).first()

    def get_user_borrowed_books(self, db: Session, user_id: int):
        user = self.get(db, id=user_id)
        if user:
            return user.borrowed_books
        return []

user = CRUDUser(User)