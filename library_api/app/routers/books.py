from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from typing import Optional
import math

from app.database import get_db
from app import models, schemas

router = APIRouter(tags=["Books"])


# ──────────────────────────────────────────────
#  GET /authors/{author_id}/books — книги автора
# ──────────────────────────────────────────────
@router.get(
    "/authors/{author_id}/books",
    response_model=schemas.PaginatedResponse,
    status_code=status.HTTP_200_OK,
)
def get_books_by_author(
    author_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    sort_by: str = Query("id", description="id | title | year"),
    sort_order: str = Query("asc"),
    genre: Optional[str] = Query(None, description="Фільтр за жанром"),
    year_from: Optional[int] = Query(None, description="Рік від"),
    year_to: Optional[int] = Query(None, description="Рік до"),
    db: Session = Depends(get_db),
):
    # Перевірка автора
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail=f"Автора з id={author_id} не знайдено")

    query = db.query(models.Book).filter(models.Book.author_id == author_id)

    # Фільтрація
    if genre:
        query = query.filter(models.Book.genre.ilike(f"%{genre}%"))
    if year_from:
        query = query.filter(models.Book.year >= year_from)
    if year_to:
        query = query.filter(models.Book.year <= year_to)

    # Сортування
    sort_fields = {"id": models.Book.id, "title": models.Book.title, "year": models.Book.year}
    sort_column = sort_fields.get(sort_by, models.Book.id)
    query = query.order_by(asc(sort_column) if sort_order == "asc" else desc(sort_column))

    # Пагінація
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": math.ceil(total / page_size) if total > 0 else 1,
        "items": [schemas.BookOut.model_validate(b) for b in items],
    }


# ──────────────────────────────────────────────
#  GET /books — всі книги (глобально)
# ──────────────────────────────────────────────
@router.get("/books", response_model=schemas.PaginatedResponse, status_code=status.HTTP_200_OK)
def get_all_books(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    sort_by: str = Query("id"),
    sort_order: str = Query("asc"),
    genre: Optional[str] = Query(None),
    title: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(models.Book)

    if genre:
        query = query.filter(models.Book.genre.ilike(f"%{genre}%"))
    if title:
        query = query.filter(models.Book.title.ilike(f"%{title}%"))

    sort_fields = {"id": models.Book.id, "title": models.Book.title, "year": models.Book.year}
    sort_column = sort_fields.get(sort_by, models.Book.id)
    query = query.order_by(asc(sort_column) if sort_order == "asc" else desc(sort_column))

    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": math.ceil(total / page_size) if total > 0 else 1,
        "items": [schemas.BookOut.model_validate(b) for b in items],
    }


# ──────────────────────────────────────────────
#  GET /authors/{author_id}/books/{book_id}
# ──────────────────────────────────────────────
@router.get(
    "/authors/{author_id}/books/{book_id}",
    response_model=schemas.BookOut,
    status_code=status.HTTP_200_OK,
)
def get_book(author_id: int, book_id: int, db: Session = Depends(get_db)):
    book = (
        db.query(models.Book)
        .filter(models.Book.id == book_id, models.Book.author_id == author_id)
        .first()
    )
    if not book:
        raise HTTPException(status_code=404, detail=f"Книгу з id={book_id} не знайдено")
    return book


# ──────────────────────────────────────────────
#  POST /authors/{author_id}/books
# ──────────────────────────────────────────────
@router.post(
    "/authors/{author_id}/books",
    response_model=schemas.BookOut,
    status_code=status.HTTP_201_CREATED,
)
def create_book(author_id: int, payload: schemas.BookCreate, db: Session = Depends(get_db)):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail=f"Автора з id={author_id} не знайдено")

    book = models.Book(**payload.model_dump(), author_id=author_id)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


# ──────────────────────────────────────────────
#  PUT /authors/{author_id}/books/{book_id}
# ──────────────────────────────────────────────
@router.put(
    "/authors/{author_id}/books/{book_id}",
    response_model=schemas.BookOut,
    status_code=status.HTTP_200_OK,
)
def update_book(
    author_id: int, book_id: int, payload: schemas.BookUpdate, db: Session = Depends(get_db)
):
    book = (
        db.query(models.Book)
        .filter(models.Book.id == book_id, models.Book.author_id == author_id)
        .first()
    )
    if not book:
        raise HTTPException(status_code=404, detail=f"Книгу з id={book_id} не знайдено")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)
    return book


# ──────────────────────────────────────────────
#  DELETE /authors/{author_id}/books/{book_id}
# ──────────────────────────────────────────────
@router.delete(
    "/authors/{author_id}/books/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_book(author_id: int, book_id: int, db: Session = Depends(get_db)):
    book = (
        db.query(models.Book)
        .filter(models.Book.id == book_id, models.Book.author_id == author_id)
        .first()
    )
    if not book:
        raise HTTPException(status_code=404, detail=f"Книгу з id={book_id} не знайдено")

    db.delete(book)
    db.commit()
