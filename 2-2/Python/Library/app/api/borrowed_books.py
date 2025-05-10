from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import Session
from app.crud.borrowed_books import borrowed_book
from app.schemas.borrowed_book import BorrowedBookCreate, BorrowedBookResponse
from app.db.database import get_session

router = APIRouter(prefix="/borrowed-books", tags=["borrowed-books"])

@router.post("/", response_model=BorrowedBookResponse)
def borrow_book(*, db: Session = Depends(get_session), borrow_in: BorrowedBookCreate):
    return borrowed_book.create(db=db, obj_in=borrow_in)

@router.get("/", response_model=List[BorrowedBookResponse])
def get_all_borrowed_books(
    *,
    db: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100
):
    return borrowed_book.get_multi(db=db, skip=skip, limit=limit)

@router.get("/active", response_model=List[BorrowedBookResponse])
def get_active_loans(*, db: Session = Depends(get_session)):
    return borrowed_book.get_active_loans(db)

@router.post("/{borrowed_book_id}/return", response_model=BorrowedBookResponse)
def return_book(*, db: Session = Depends(get_session), borrowed_book_id: int):
    db_borrowed_book = borrowed_book.get(db=db, id=borrowed_book_id)
    if not db_borrowed_book:
        raise HTTPException(status_code=404, detail="Borrowed book record not found")
    if db_borrowed_book.returned_date:
        raise HTTPException(status_code=400, detail="Book already returned")
    return borrowed_book.return_book(db=db, borrowed_book_id=borrowed_book_id)

@router.get("/{borrowed_book_id}", response_model=BorrowedBookResponse)
def get_borrowed_book(*, db: Session = Depends(get_session), borrowed_book_id: int):
    db_borrowed_book = borrowed_book.get(db=db, id=borrowed_book_id)
    if not db_borrowed_book:
        raise HTTPException(status_code=404, detail="Borrowed book record not found")
    return db_borrowed_book