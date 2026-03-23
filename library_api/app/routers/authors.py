from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from typing import Optional
import math

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/authors", tags=["Authors"])


# ──────────────────────────────────────────────
#  GET /authors — список авторів з пагінацією,
#                 сортуванням та фільтрацією
# ──────────────────────────────────────────────
@router.get("/", response_model=schemas.PaginatedResponse, status_code=status.HTTP_200_OK)
def get_authors(
    page: int = Query(1, ge=1, description="Номер сторінки"),
    page_size: int = Query(10, ge=1, le=100, description="Кількість на сторінці"),
    sort_by: str = Query("id", description="Поле сортування: id | name | nationality"),
    sort_order: str = Query("asc", description="Напрямок: asc | desc"),
    nationality: Optional[str] = Query(None, description="Фільтр за національністю"),
    name: Optional[str] = Query(None, description="Пошук по імені (часткове співпадіння)"),
    db: Session = Depends(get_db),
):
    query = db.query(models.Author)

    # Фільтрація
    if nationality:
        query = query.filter(models.Author.nationality.ilike(f"%{nationality}%"))
    if name:
        query = query.filter(models.Author.name.ilike(f"%{name}%"))

    # Сортування
    sort_fields = {"id": models.Author.id, "name": models.Author.name, "nationality": models.Author.nationality}
    sort_column = sort_fields.get(sort_by, models.Author.id)
    query = query.order_by(asc(sort_column) if sort_order == "asc" else desc(sort_column))

    # Пагінація
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": math.ceil(total / page_size) if total > 0 else 1,
        "items": [schemas.AuthorOut.model_validate(a) for a in items],
    }


# ──────────────────────────────────────────────
#  GET /authors/{id} — один автор
# ──────────────────────────────────────────────
@router.get("/{author_id}", response_model=schemas.AuthorOut, status_code=status.HTTP_200_OK)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail=f"Автора з id={author_id} не знайдено")
    return author


# ──────────────────────────────────────────────
#  POST /authors — створити автора
# ──────────────────────────────────────────────
@router.post("/", response_model=schemas.AuthorOut, status_code=status.HTTP_201_CREATED)
def create_author(payload: schemas.AuthorCreate, db: Session = Depends(get_db)):
    author = models.Author(**payload.model_dump())
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


# ──────────────────────────────────────────────
#  PUT /authors/{id} — повне оновлення
# ──────────────────────────────────────────────
@router.put("/{author_id}", response_model=schemas.AuthorOut, status_code=status.HTTP_200_OK)
def update_author(author_id: int, payload: schemas.AuthorUpdate, db: Session = Depends(get_db)):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail=f"Автора з id={author_id} не знайдено")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(author, field, value)

    db.commit()
    db.refresh(author)
    return author


# ──────────────────────────────────────────────
#  DELETE /authors/{id} — видалити автора
# ──────────────────────────────────────────────
@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail=f"Автора з id={author_id} не знайдено")
    db.delete(author)
    db.commit()
