from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import Session
from app.db.database import get_session
from app.models.associations import BookAuthor, BookCategory
from app.models.book import Book
from app.models.author import Author
from app.models.category import Category
from sqlmodel import select

router = APIRouter(prefix="/associations", tags=["associations"])

@router.post("/book-author")
def create_book_author_association(
    *, db: Session = Depends(get_session), book_id: int, author_id: int
):
    book = db.exec(select(Book).where(Book.id == book_id)).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    author = db.exec(select(Author).where(Author.id == author_id)).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    association = BookAuthor(book_id=book_id, author_id=author_id)
    db.add(association)
    db.commit()
    return {"message": "Book-author association created successfully"}

@router.post("/book-category")
def create_book_category_association(
    *, db: Session = Depends(get_session), book_id: int, category_id: int
):
    book = db.exec(select(Book).where(Book.id == book_id)).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    category = db.exec(select(Category).where(Category.id == category_id)).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    association = BookCategory(book_id=book_id, category_id=category_id)
    db.add(association)
    db.commit()
    return {"message": "Book-category association created successfully"}

@router.delete("/book-author")
def delete_book_author_association(
    *, db: Session = Depends(get_session), book_id: int, author_id: int
):
    association = db.exec(
        select(BookAuthor)
        .where(BookAuthor.book_id == book_id)
        .where(BookAuthor.author_id == author_id)
    ).first()
    
    if not association:
        raise HTTPException(status_code=404, detail="Association not found")
    
    db.delete(association)
    db.commit()
    return {"message": "Book-author association deleted successfully"}

@router.delete("/book-category")
def delete_book_category_association(
    *, db: Session = Depends(get_session), book_id: int, category_id: int
):
    association = db.exec(
        select(BookCategory)
        .where(BookCategory.book_id == book_id)
        .where(BookCategory.category_id == category_id)
    ).first()
    
    if not association:
        raise HTTPException(status_code=404, detail="Association not found")
    
    db.delete(association)
    db.commit()
    return {"message": "Book-category association deleted successfully"}

@router.get("/book/{book_id}/authors")
def get_book_authors(*, db: Session = Depends(get_session), book_id: int):
    book = db.exec(select(Book).where(Book.id == book_id)).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book.authors

@router.get("/book/{book_id}/categories")
def get_book_categories(*, db: Session = Depends(get_session), book_id: int):
    book = db.exec(select(Book).where(Book.id == book_id)).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book.categories