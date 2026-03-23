from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Author(Base):
    """Сутність: Автор"""
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    biography = Column(Text, nullable=True)
    nationality = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Зв'язок: один автор → багато книг
    books = relationship("Book", back_populates="author", cascade="all, delete-orphan")


class Book(Base):
    """Сутність: Книга (вкладена в Автора)"""
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    genre = Column(String(50), nullable=True)
    year = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Зв'язок: багато книг → один автор
    author = relationship("Author", back_populates="books")

    # Зв'язок: одна книга → багато відгуків
    reviews = relationship("Review", back_populates="book", cascade="all, delete-orphan")


class Review(Base):
    """Сутність: Відгук (вкладений в Книгу)"""
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    reviewer_name = Column(String(100), nullable=False)
    rating = Column(Float, nullable=False)   # 1.0 – 5.0
    comment = Column(Text, nullable=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Зв'язок: багато відгуків → одна книга
    book = relationship("Book", back_populates="reviews")
