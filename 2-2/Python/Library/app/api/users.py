from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import Session
from app.crud.users import user
from app.schemas.user import UserCreate, UserResponse
from app.schemas.borrowed_book import BorrowedBookResponse
from app.db.database import get_session
from app.utils.auth import get_current_user

router = APIRouter()

# Перемістили ендпоінт /me на початок, щоб він не конфліктував з /{user_id}
@router.get("/me")
async def read_users_me(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    db_user = user.get_by_email(db, email=current_user["email"])
    if not db_user:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")
    
    return {
        "email": db_user.email,
        "first_name": db_user.first_name,
        "last_name": db_user.last_name
    }

@router.post("/", response_model=UserResponse)
def create_user(*, db: Session = Depends(get_session), user_in: UserCreate):
    existing_user = user.get_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user.create(db=db, obj_in=user_in)

@router.get("/", response_model=List[UserResponse])
def get_users(
    *,
    db: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100
):
    return user.get_multi(db=db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(*, db: Session = Depends(get_session), user_id: int):
    db_user = user.get(db=db, id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/{user_id}/borrowed_books", response_model=List[BorrowedBookResponse])
def get_user_borrowed_books(*, db: Session = Depends(get_session), user_id: int):
    db_user = user.get(db=db, id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.get_user_borrowed_books(db=db, user_id=user_id)

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    *,
    db: Session = Depends(get_session),
    user_id: int,
    user_in: UserCreate
):
    db_user = user.get(db=db, id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.update(db=db, db_obj=db_user, obj_in=user_in)

@router.delete("/{user_id}", response_model=UserResponse)
def delete_user(*, db: Session = Depends(get_session), user_id: int):
    db_user = user.get(db=db, id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.remove(db=db, id=user_id)