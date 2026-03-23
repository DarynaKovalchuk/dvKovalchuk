from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import authors, books, reviews

# Автоматично створює таблиці при старті
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="📚 Library REST API",
    description="""
## Система управління бібліотекою

### Сутності та зв'язки:
- **Author** (Автор) → має багато **Book** (Книг)
- **Book** (Книга) → має багато **Review** (Відгуків)

### Функціонал:
- ✅ CRUD для кожної сутності
- ✅ Пагінація (page / page_size)
- ✅ Сортування (sort_by / sort_order)
- ✅ Фільтрація (name, nationality, genre, rating тощо)
- ✅ Вкладені ресурси (nested routes)
    """,
    version="1.0.0",
)

# CORS (дозволяє запити з браузера / фронтенду)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Підключення роутерів
app.include_router(authors.router, prefix="/api/v1")
app.include_router(books.router, prefix="/api/v1")
app.include_router(reviews.router, prefix="/api/v1")


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Library API працює!",
        "docs": "/docs",
        "redoc": "/redoc",
    }
