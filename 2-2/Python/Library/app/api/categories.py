from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import Session
from app.crud.categories import category
from app.schemas.category import CategoryCreate, CategoryResponse
from app.db.database import get_session

router = APIRouter(prefix="/categories", tags=["categories"])

@router.post("/", response_model=CategoryResponse)
def create_category(*, db: Session = Depends(get_session), category_in: CategoryCreate):
    existing_category = category.get_by_name(db, name=category_in.name)
    if existing_category:
        raise HTTPException(status_code=400, detail="Category already exists")
    return category.create(db=db, obj_in=category_in)

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(*, db: Session = Depends(get_session), category_id: int):
    db_category = category.get(db=db, id=category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.get("/", response_model=List[CategoryResponse])
def get_categories(
    *,
    db: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100
):
    return category.get_multi(db=db, skip=skip, limit=limit)

@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    *,
    db: Session = Depends(get_session),
    category_id: int,
    category_in: CategoryCreate
):
    db_category = category.get(db=db, id=category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category.update(db=db, db_obj=db_category, obj_in=category_in)

@router.delete("/{category_id}", response_model=CategoryResponse)
def delete_category(*, db: Session = Depends(get_session), category_id: int):
    db_category = category.get(db=db, id=category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category.remove(db=db, id=category_id)