from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import Session
from app.crud.books import book
from app.schemas.book import BookCreate, BookResponse
from app.db.database import get_session
from app.models.associations import BookAuthor, BookCategory
from app.models.book import Book
from app.models.author import Author
from app.models.category import Category

router = APIRouter(prefix="/books", tags=["books"])

@router.post("/", response_model=BookResponse)
def create_book(*, db: Session = Depends(get_session), book_in: BookCreate):
    try:
        # Check if book exists
        existing_book = book.get_by_isbn(db, isbn=book_in.isbn)
        if existing_book:
            raise HTTPException(status_code=400, detail="Book with this ISBN already exists")
        
        # Create new book
        new_book = Book(
            title=book_in.title,
            publication_year=book_in.publication_year,
            isbn=book_in.isbn,
            copies_available=book_in.copies_available
        )
        db.add(new_book)
        db.flush()  # Get the new book ID

        # Create author relationships
        for author_id in book_in.author_ids:
            author = db.query(Author).filter(Author.id == author_id).first()
            if not author:
                raise HTTPException(status_code=404, detail=f"Author with id {author_id} not found")
            book_author = BookAuthor(book_id=new_book.id, author_id=author_id)
            db.add(book_author)

        # Create category relationships
        for category_id in book_in.category_ids:
            category = db.query(Category).filter(Category.id == category_id).first()
            if not category:
                raise HTTPException(status_code=404, detail=f"Category with id {category_id} not found")
            book_category = BookCategory(book_id=new_book.id, category_id=category_id)
            db.add(book_category)

        db.commit()
        db.refresh(new_book)
        return new_book
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{book_id}", response_model=BookResponse)
def get_book(*, db: Session = Depends(get_session), book_id: int):
    db_book = book.get(db=db, id=book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.get("/", response_model=List[BookResponse])
def get_books(
    *,
    db: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100
):
    return book.get_multi(db=db, skip=skip, limit=limit)

@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    *,
    db: Session = Depends(get_session),
    book_id: int,
    book_in: BookCreate
):
    db_book = book.get(db=db, id=book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book.update(db=db, db_obj=db_book, obj_in=book_in)

@router.delete("/{book_id}", response_model=BookResponse)
def delete_book(*, db: Session = Depends(get_session), book_id: int):
    db_book = book.get(db=db, id=book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book.remove(db=db, id=book_id)