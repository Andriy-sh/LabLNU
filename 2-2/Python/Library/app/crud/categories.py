from sqlmodel import select
from app.crud.base import CRUDBase
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse
from sqlmodel.ext.asyncio.session import Session

class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryResponse]):
    def get_by_name(self, db: Session, name: str) -> Category:
        return db.exec(select(Category).where(Category.name == name)).first()

category = CRUDCategory(Category)