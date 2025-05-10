from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import Session
from app.crud.authors import author
from app.schemas.author import AuthorCreate, AuthorResponse
from app.db.database import get_session

router = APIRouter(prefix="/authors", tags=["authors"])

@router.post("/", response_model=AuthorResponse)
def create_author(*, db: Session = Depends(get_session), author_in: AuthorCreate):
    existing_author = author.get_by_name(
        db, first_name=author_in.first_name, last_name=author_in.last_name
    )
    if existing_author:
        raise HTTPException(status_code=400, detail="Author already exists")
    return author.create(db=db, obj_in=author_in)

@router.get("/{author_id}", response_model=AuthorResponse)
def get_author(*, db: Session = Depends(get_session), author_id: int):
    db_author = author.get(db=db, id=author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author

@router.get("/", response_model=List[AuthorResponse])
def get_authors(
    *,
    db: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100
):
    return author.get_multi(db=db, skip=skip, limit=limit)

@router.put("/{author_id}", response_model=AuthorResponse)
def update_author(
    *,
    db: Session = Depends(get_session),
    author_id: int,
    author_in: AuthorCreate
):
    db_author = author.get(db=db, id=author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author.update(db=db, db_obj=db_author, obj_in=author_in)

@router.delete("/{author_id}", response_model=AuthorResponse)
def delete_author(*, db: Session = Depends(get_session), author_id: int):
    db_author = author.get(db=db, id=author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author.remove(db=db, id=author_id)