from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


# ──────────────────────────────────────────────
#  REVIEW schemas
# ──────────────────────────────────────────────

class ReviewBase(BaseModel):
    reviewer_name: str = Field(..., min_length=2, max_length=100, example="Іван Франко")
    rating: float = Field(..., ge=1.0, le=5.0, example=4.5)
    comment: Optional[str] = Field(None, example="Чудова книга!")

    @field_validator("rating")
    @classmethod
    def round_rating(cls, v):
        return round(v, 1)


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    reviewer_name: Optional[str] = Field(None, min_length=2, max_length=100)
    rating: Optional[float] = Field(None, ge=1.0, le=5.0)
    comment: Optional[str] = None


class ReviewOut(ReviewBase):
    id: int
    book_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ──────────────────────────────────────────────
#  BOOK schemas
# ──────────────────────────────────────────────

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, example="Кобзар")
    genre: Optional[str] = Field(None, max_length=50, example="Поезія")
    year: Optional[int] = Field(None, ge=0, le=2100, example=1840)
    description: Optional[str] = Field(None, example="Збірка поезій Тараса Шевченка")


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    genre: Optional[str] = None
    year: Optional[int] = Field(None, ge=0, le=2100)
    description: Optional[str] = None


class BookOut(BookBase):
    id: int
    author_id: int
    created_at: datetime
    reviews: List[ReviewOut] = []

    model_config = {"from_attributes": True}


class BookOutShort(BookBase):
    """Коротка версія книги (без відгуків) — для списку авторів"""
    id: int
    author_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ──────────────────────────────────────────────
#  AUTHOR schemas
# ──────────────────────────────────────────────

class AuthorBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, example="Тарас Шевченко")
    biography: Optional[str] = Field(None, example="Великий український поет")
    nationality: Optional[str] = Field(None, max_length=50, example="Українська")


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    biography: Optional[str] = None
    nationality: Optional[str] = None


class AuthorOut(AuthorBase):
    id: int
    created_at: datetime
    books: List[BookOutShort] = []

    model_config = {"from_attributes": True}


# ──────────────────────────────────────────────
#  PAGINATION wrapper
# ──────────────────────────────────────────────

class PaginatedResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    items: list
