from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
import math

from app.database import get_db
from app import models, schemas

router = APIRouter(tags=["Reviews"])


def _get_book_or_404(book_id: int, db: Session) -> models.Book:
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail=f"Книгу з id={book_id} не знайдено")
    return book


# ──────────────────────────────────────────────
#  GET /books/{book_id}/reviews
# ──────────────────────────────────────────────
@router.get(
    "/books/{book_id}/reviews",
    response_model=schemas.PaginatedResponse,
    status_code=status.HTTP_200_OK,
)
def get_reviews(
    book_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    sort_by: str = Query("id", description="id | rating | created_at"),
    sort_order: str = Query("desc"),
    min_rating: float = Query(None, ge=1.0, le=5.0, description="Мінімальний рейтинг"),
    db: Session = Depends(get_db),
):
    _get_book_or_404(book_id, db)

    query = db.query(models.Review).filter(models.Review.book_id == book_id)

    # Фільтрація
    if min_rating is not None:
        query = query.filter(models.Review.rating >= min_rating)

    # Сортування
    sort_fields = {
        "id": models.Review.id,
        "rating": models.Review.rating,
        "created_at": models.Review.created_at,
    }
    sort_column = sort_fields.get(sort_by, models.Review.id)
    query = query.order_by(asc(sort_column) if sort_order == "asc" else desc(sort_column))

    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": math.ceil(total / page_size) if total > 0 else 1,
        "items": [schemas.ReviewOut.model_validate(r) for r in items],
    }


# ──────────────────────────────────────────────
#  GET /books/{book_id}/reviews/{review_id}
# ──────────────────────────────────────────────
@router.get(
    "/books/{book_id}/reviews/{review_id}",
    response_model=schemas.ReviewOut,
    status_code=status.HTTP_200_OK,
)
def get_review(book_id: int, review_id: int, db: Session = Depends(get_db)):
    _get_book_or_404(book_id, db)
    review = (
        db.query(models.Review)
        .filter(models.Review.id == review_id, models.Review.book_id == book_id)
        .first()
    )
    if not review:
        raise HTTPException(status_code=404, detail=f"Відгук з id={review_id} не знайдено")
    return review


# ──────────────────────────────────────────────
#  POST /books/{book_id}/reviews
# ──────────────────────────────────────────────
@router.post(
    "/books/{book_id}/reviews",
    response_model=schemas.ReviewOut,
    status_code=status.HTTP_201_CREATED,
)
def create_review(book_id: int, payload: schemas.ReviewCreate, db: Session = Depends(get_db)):
    _get_book_or_404(book_id, db)
    review = models.Review(**payload.model_dump(), book_id=book_id)
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


# ──────────────────────────────────────────────
#  PUT /books/{book_id}/reviews/{review_id}
# ──────────────────────────────────────────────
@router.put(
    "/books/{book_id}/reviews/{review_id}",
    response_model=schemas.ReviewOut,
    status_code=status.HTTP_200_OK,
)
def update_review(
    book_id: int, review_id: int, payload: schemas.ReviewUpdate, db: Session = Depends(get_db)
):
    _get_book_or_404(book_id, db)
    review = (
        db.query(models.Review)
        .filter(models.Review.id == review_id, models.Review.book_id == book_id)
        .first()
    )
    if not review:
        raise HTTPException(status_code=404, detail=f"Відгук з id={review_id} не знайдено")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(review, field, value)

    db.commit()
    db.refresh(review)
    return review


# ──────────────────────────────────────────────
#  DELETE /books/{book_id}/reviews/{review_id}
# ──────────────────────────────────────────────
@router.delete(
    "/books/{book_id}/reviews/{review_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_review(book_id: int, review_id: int, db: Session = Depends(get_db)):
    _get_book_or_404(book_id, db)
    review = (
        db.query(models.Review)
        .filter(models.Review.id == review_id, models.Review.book_id == book_id)
        .first()
    )
    if not review:
        raise HTTPException(status_code=404, detail=f"Відгук з id={review_id} не знайдено")

    db.delete(review)
    db.commit()
