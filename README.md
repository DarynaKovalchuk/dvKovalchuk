# dvKovalchuk
ЛАБОРАТОРНА 1 -------------------------------------------------
1. Породжувальний шаблон - Фабричний метод (Factory Method)
Проблема
Нехай необхідний застосунок для логістики. Спочатку він працює лише з вантажівками (Truck). Через деякий час потрібно додати морські перевезення (Ship). Якщо скрізь у коді прописано new Truck(), то додавання нового класу змушує переписувати більшість існуючого коду - він сильно пов'язаний з конкретним класом.
Фабричний метод вирішує цю проблему: він виносить створення об'єктів у спеціальний метод, який підкласи можуть перевизначати. Клієнтський код більше не залежить від конкретних класів.
Ідея реалізації
Оголошується інтерфейс (абстрактний клас) для продукту (Transport).
Оголошується Creator з абстрактним factory_method().
Кожен ConcreteCreator перевизначає factory_method() і повертає свій тип продукту.
Клієнтський код викликає factory_method() через інтерфейс Creator, не знаючи, який саме об'єкт буде створено.
```python
from abc import ABC, abstractmethod

# ─── Продукти ────────────────────────────────────────────────────
class Transport(ABC):
    @abstractmethod
    def deliver(self) -> str:
        pass

class Truck(Transport):
    def deliver(self) -> str:
        return "Truck Доставка вантажівкою по дорозі"

class Ship(Transport):
    def deliver(self) -> str:
        return "Ship Доставка кораблем по морю"

class Plane(Transport):
    def deliver(self) -> str:
        return "Plane  Доставка літаком по повітрю"


# ─── Creators ────────────────────────────────────────────────────
class Logistics(ABC):
    @abstractmethod
    def factory_method(self) -> Transport:
        """Фабричний метод — підкласи перевизначають цей метод."""
        pass

    def plan_delivery(self) -> str:
        # Загальна логіка, яка використовує продукт через інтерфейс
        transport = self.factory_method()
        return f"Логістика: отримано транспорт → {transport.deliver()}"

class RoadLogistics(Logistics):
    def factory_method(self) -> Transport:
        return Truck()

class SeaLogistics(Logistics):
    def factory_method(self) -> Transport:
        return Ship()

class AirLogistics(Logistics):
    def factory_method(self) -> Transport:
        return Plane()


# ─── Клієнтський код ─────────────────────────────────────────────
def client_code(logistics: Logistics) -> None:
    print(logistics.plan_delivery())

if __name__ == "__main__":
    print("=== Фабричний метод ===")
    for provider in [RoadLogistics(), SeaLogistics(), AirLogistics()]:
        client_code(provider)



'''
┌─────────────────────┐         ┌──────────────────┐
│  <<abstract>>       │         │  <<abstract>>    │
│  Logistics          │         │  Transport       │
│─────────────────────│         │──────────────────│
│ + factory_method()  │────────►│ + deliver(): str │
│ + plan_delivery()   │         └──────────────────┘
└─────────────────────┘                  ▲
         ▲                      ┌────────┼─────────┐
         │                      │        │         │
┌────────┼────────┐          ┌──┴──┐  ┌──┴─┐  ┌───┴──┐
│        │        │          │Truck│  │Ship│  │Plane │
│        │        │          │─────│  │────│  │──────│
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ RoadLogistics│  │ SeaLogistics │  │ AirLogistics │
│──────────────│  │──────────────│  │──────────────│
│factory_method│  │factory_method│  │factory_method│
│ → Truck()    │  │ → Ship()     │  │ → Plane()    │
└──────────────┘  └──────────────┘  └──────────────┘
'''
```

2. Структурний шаблон - Міст (Bridge)
Проблема
Нехай є фігури: Circle і Square. Тепер потрібно додати кольори: Red і Blue. Без шаблону «Міст» виникне комбінаторний вибух класів: RedCircle, BlueCircle, RedSquare, BlueSquare. Якщо додати третій колір - ще 2 класи. Якщо третю фігуру - ще 3 класи.
Міст розділяє ієрархію на два незалежні виміри: абстракцію (що робимо) та реалізацію (як робимо). Замість успадкування - композиція через агрегацію.
Ідея реалізації
Код розділений на два незалежні виміри, які з'єднані через поле self.color - це і є «міст»:
Вимір 1 - Абстракція (фігури): абстрактний клас Shape зберігає посилання на об'єкт Color і делегує йому відповідальність за колір. Конкретні фігури (Circle, Square, Triangle) лише реалізують метод draw(), всередині якого звертаються до self.color.fill() - але не знають, який саме колір там буде.
Вимір 2 - Реалізація (кольори): абстрактний клас Color оголошує метод fill(). Конкретні кольори (Red, Blue, Green) повертають свою назву. Вони нічого не знають про фігури.
Завдяки такому розділенню, щоб додати новий колір - достатньо створити один клас-спадкоємець Color. Щоб додати нову фігуру - один клас-спадкоємець Shape. Жодна зміна в одному вимірі не зачіпає інший.
```python
from abc import ABC, abstractmethod

# ─── Implementation — кольори ─────────────────────────────────────
class Color(ABC):
    @abstractmethod
    def fill(self) -> str:
        pass

class Red(Color):
    def fill(self) -> str:
        return "червоним"

class Blue(Color):
    def fill(self) -> str:
        return "синім"

class Green(Color):
    def fill(self) -> str:
        return "зеленим"


# ─── Abstraction — фігури ─────────────────────────────────────────
class Shape(ABC):
    def __init__(self, color: Color):
        self.color = color  # ← "Міст" до реалізації

    @abstractmethod
    def draw(self) -> str:
        pass

class Circle(Shape):
    def draw(self) -> str:
        return f"Коло, зафарбоване {self.color.fill()}"

class Square(Shape):
    def draw(self) -> str:
        return f"Квадрат, зафарбований {self.color.fill()}"

class Triangle(Shape):
    def draw(self) -> str:
        return f"Трикутник, зафарбований {self.color.fill()}"


if __name__ == "__main__":
    print("=== Шаблон Міст: фігури + кольори ===\n")

    shapes = [
        Circle(Red()),
        Circle(Blue()),
        Square(Red()),
        Square(Green()),
        Triangle(Blue()),
        Triangle(Green()),
    ]

    for shape in shapes:
        print(shape.draw())

    print("\n--- Зміна кольору «на льоту» ---")
    my_circle = Circle(Red())
    print(f"До:    {my_circle.draw()}")
    my_circle.color = Blue()
    print(f"Після: {my_circle.draw()}")

'''
АБСТРАКЦІЯ                          РЕАЛІЗАЦІЯ
─────────────────────────────       ────────────────────────
                                    
┌────────────────────────────┐      ┌────────────────────┐
│      Shape                 │      │      Color         │
│  <<abstract>>              │      │   <<abstract>>     │
│────────────────────────────│      │────────────────────│
│ - color: Color             │─────►│ + fill(): str      │
│────────────────────────────│      └────────────────────┘
│ + __init__(color: Color)   │                ▲
│ + draw(): str              │       ┌────────┼────────┐
└────────────────────────────┘       │        │        │
              ▲                   ┌──┴──┐  ┌──┴──┐  ┌──┴───┐
    ┌─────────┼─────────┐         │ Red │  │Blue │  │Green │
    │         │         │         │─────│  │─────│  │──────│
┌───┴──┐  ┌───┴──┐  ┌───┴────┐    │fill │  │fill │  │fill  │
│Circle│  │Square│  │Triangle│    │→    │  │→    │  │→     │
│──────│  │──────│  │────────│    │"чер"│  │"син"│  │"зел" │
│draw()│  │draw()│  │draw()  │    └─────┘  └─────┘  └──────┘
└──────┘  └──────┘  └────────┘
'''
```

3. Поведінковий шаблон - Ланцюжок обов'язків (Chain of Responsibility)
Проблема
У системі обробки запитів часто потрібно кілька рівнів перевірки або обробки підряд: автентифікація → авторизація → валідація → кешування → бізнес-логіка. Якщо жорстко зв'язати їх в одному місці — код стає монолітним, важко розширювати і тестувати кожен рівень окремо.
Ланцюжок обов'язків пропонує передавати запит через ланцюжок обробників. Кожен обробник вирішує: опрацювати запит самостійно чи передати далі по ланцюжку. Відправник не знає, хто саме обробить запит.
Ідея реалізації
Кожен Handler зберігає посилання на наступний обробник (next_handler).
Метод handle() або обробляє запит, або викликає next_handler.handle().
Клієнт складає ланцюжок у потрібному порядку та відправляє запит першому.
```python
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional
import time

# ─── Базовий Handler ─────────────────────────────────────────────
class Handler(ABC):
    def __init__(self):
        self._next: Optional[Handler] = None

    def set_next(self, handler: Handler) -> Handler:
        """Повертає handler для зручного ланцюжкового виклику."""
        self._next = handler
        return handler

    def handle(self, request: dict) -> Optional[str]:
        if self._next:
            return self._next.handle(request)
        return None  # Кінець ланцюжка — ніхто не обробив


# ─── Конкретні обробники ──────────────────────────────────────────
class AuthHandler(Handler):
    """Перевіряє наявність та коректність токена."""
    VALID_TOKENS = {"secret-token-123", "admin-token-456"}

    def handle(self, request: dict) -> Optional[str]:
        token = request.get("token", "")
        if token not in self.VALID_TOKENS:
            return f"AuthHandler: відхилено — невалідний токен '{token}'"
        print(f"AuthHandler: токен валідний")
        return super().handle(request)


class RateLimitHandler(Handler):
    """Обмежує кількість запитів (проста in-memory реалізація)."""
    def __init__(self, max_requests: int = 3):
        super().__init__()
        self.max_requests = max_requests
        self._counts: dict[str, int] = {}

    def handle(self, request: dict) -> Optional[str]:
        user = request.get("user", "anonymous")
        self._counts[user] = self._counts.get(user, 0) + 1
        if self._counts[user] > self.max_requests:
            return f"RateLimitHandler: ліміт запитів вичерпано для '{user}'"
        print(f"RateLimitHandler: запит {self._counts[user]}/{self.max_requests}")
        return super().handle(request)


class ValidationHandler(Handler):
    """Перевіряє обов'язкові поля запиту."""
    REQUIRED_FIELDS = ["action", "data"]

    def handle(self, request: dict) -> Optional[str]:
        missing = [f for f in self.REQUIRED_FIELDS if f not in request]
        if missing:
            return f"ValidationHandler: відсутні поля: {missing}"
        print(f"ValidationHandler: всі поля присутні")
        return super().handle(request)


class BusinessLogicHandler(Handler):
    """Кінцевий обробник — виконує бізнес-логіку."""
    def handle(self, request: dict) -> Optional[str]:
        action = request["action"]
        data = request["data"]
        result = f"BusinessLogic: виконано '{action}' з даними: {data}"
        print(result)
        return result


# ─── Клієнтський код ─────────────────────────────────────────────
def process_request(chain: Handler, request: dict) -> None:
    print(f"\n--- Запит: {request} ---")
    result = chain.handle(request)
    if result:
        print(f"Результат: {result}")

if __name__ == "__main__":
    print("=== Ланцюжок обов'язків ===")

    # Збираємо ланцюжок
    auth     = AuthHandler()
    rate     = RateLimitHandler(max_requests=2)
    validate = ValidationHandler()
    business = BusinessLogicHandler()

    auth.set_next(rate).set_next(validate).set_next(business)

    # Тест 1: коректний запит
    process_request(auth, {
        "token": "secret-token-123",
        "user": "alice",
        "action": "create",
        "data": {"name": "Item A"}
    })

    # Тест 2: другий запит від alice (досягає ліміту)
    process_request(auth, {
        "token": "secret-token-123",
        "user": "alice",
        "action": "read",
        "data": {"id": 1}
    })

    # Тест 3: третій запит — ліміт перевищено
    process_request(auth, {
        "token": "secret-token-123",
        "user": "alice",
        "action": "delete",
        "data": {"id": 1}
    })

    # Тест 4: невалідний токен
    process_request(auth, {
        "token": "wrong-token",
        "user": "eve",
        "action": "hack",
        "data": {}
    })

    # Тест 5: відсутні обов'язкові поля
    process_request(auth, {
        "token": "admin-token-456",
        "user": "bob"
    })

    '''
    Client ──► [AuthHandler] ──► [RateLimitHandler] ──► [ValidationHandler] ──► [BusinessHandler]
                │                    │                       │                       │
          перевіряє токен      рахує запити           перевіряє поля         виконує логіку
          якщо ні → стоп       якщо ліміт → стоп      якщо немає → стоп

┌──────────────────────────────────┐
│  <<abstract>> Handler            │
│──────────────────────────────────│
│ - _next: Handler                 │
│ + set_next(handler) -> Handler   │
│ + handle(request) -> str | None  │
└──────────────────────────────────┘
              ▲
    ┌─────────┼──────────────┐
    │         │              │
┌───┴───┐ ┌───┴──────┐  ┌────┴──────────┐ ┌───────────────┐
│ Auth  │ │RateLimit │  │  Validation   │ │ BusinessLogic │
│Handler│ │ Handler  │  │    Handler    │ │    Handler    │
└───────┘ └──────────┘  └───────────────┘ └───────────────┘
    '''
```



ЛАБОРАТОРНА 2 ---------------------------------------------------------

1.Технології:
Python 3.12 — мова програмування
FastAPI — веб-фреймворк для побудови API
SQLAlchemy — ORM для роботи з базою даних
SQLite — база даних
Uvicorn — ASGI-сервер для запуску застосунку

2. Структура проекту
```
library_api/
├── main.py             
├── requirements.txt     
├── .env                 
├── test_api.http        
└── app/
    ├── database.py      
    ├── models.py        
    ├── schemas.py       
    └── routers/
        ├── authors.py   
        ├── books.py     
        └── reviews.py
```

4. Сутності та зв'язки між ними
```
В системі реалізовано 3 сутності з такими зв'язками:
Author (Автор)
    │
    │  один автор має багато книг
    ▼
Book (Книга)
    │
    │  одна книга має багато відгуків
    ▼
Review (Відгук)
```

6. POST — Створення записів
```
   ### 4. Створити автора
POST {{BASE}}/authors
Content-Type: application/json

{
  "name": "Тарас Шевченко",
  "biography": "Великий український поет, художник і мислитель.",
  "nationality": "Українська"
}

Результат:
HTTP/1.1 201 Created

{
  "id": 1,
  "name": "Тарас Шевченко",
  "biography": "Великий український поет, художник і мислитель.",
  "nationality": "Українська",
  "created_at": "2024-01-15T10:30:00",
  "books": []
}
```

5. GET — Отримання даних
```
### 5. Отримати одного автора
GET {{BASE}}/authors/1

Результат:
HTTP/1.1 200 OK

{
  "title": "Кобзар",
  "genre": "Поезія",
  "year": 1840,
  "description": "Збірка поетичних творів Тараса Шевченка",
  "id": 1,
  "author_id": 1,
  "created_at": "2026-03-23T14:29:23",
  "reviews": []
}
```

6. DELETE — Видалення запису
```
DELETE {{BASE}}/books/1/reviews/1`

Результат:
HTTP/1.1 204 No Content
```

7. PUT - Оновити автора
```
PUT {{BASE}}/authors/1
Content-Type: application/json

{
  "biography": "Оновлена біографія Тараса Шевченка"
}

Результат:
{
  "name": "Тарас Шевченко",
  "biography": "Великий український поет, художник і мислитель.",
  "nationality": "Українська",
  "id": 1,
  "created_at": "2026-03-23T14:23:46",
  "books": [
    {
      "title": "Кобзар",
      "genre": "Поезія",
      "year": 1840,
      "description": "Збірка поетичних творів Тараса Шевченка",
      "id": 1,
      "author_id": 1,
      "created_at": "2026-03-23T14:29:23"
    }
}
```

8. Пагінація
```
### 1. Отримати всіх авторів (з пагінацією)
GET {{BASE}}/authors?page=1&page_size=5:
json{
  "total": 2,
  "page": 1,
  "page_size": 5,
  "total_pages": 1,
  "items": [...]
}
```

9. Сортування
```
### 1. Отримати авторів із сортуванням та фільтрацією
GET {{BASE}}/authors?sort_by=name&sort_order=asc
### 2. Отримати книги з фільтрацією по жанру і сортуванням
GET {{BASE}}/authors/1/books?sort_by=year&sort_order=asc
```

10. Фільтрація
```
### 1. Пошук автора по імені
GET {{BASE}}/authors?name=Шевченко
### 2. Фільтр по жанру:
GET {{BASE}}/authors/1/books?genre=Поезія
### 3. Фільтрація відгуків за мінімальним рейтингом
GET {{BASE}}/books/1/reviews?min_rating=4.0
```


ЛАБОРАТОРНА 3 ---------------------------------------------------------------
```
lab3/
│
├── app.py                                                        
│
├── requirements.txt             
│
└── templates/                    
    │
    ├── base.html                 
    │
    ├── login.html             
    │
    ├── dashboard.html            
    │
    ├── notes.html                
    │
    └── profile.html
```

Загальний опис
Проект є клієнт-серверним веб-застосунком, реалізованим на основі фреймворку Flask (Python). Застосунок імітує особистий кабінет користувача з системою авторизації, навігацією між сторінками та збереженням спільного стану.

Технічний стек
Бекенд — Python, Flask. Відповідає за маршрутизацію, авторизацію, зберігання сесій та обробку API-запитів.
Фронтенд — HTML, CSS, JavaScript. Усі сторінки наслідують базовий шаблон base.html.

Сторінки застосунку
Сторінка входу (/login) — форма авторизації з полями логіну та паролю. При успішному вході користувач перенаправляється на головну панель. При помилці відображається повідомлення без перезавантаження сторінки.
<img width="1232" height="1190" alt="regestration" src="https://github.com/user-attachments/assets/1ab6881d-fb22-4579-ad29-f151b0184954" />


Головна панель (/dashboard) — відображає інформацію про поточного користувача: ім’я, роль, кількість нотаток та збережений токен авторизації. Слугує точкою входу після авторизації.
<img width="1232" height="1190" alt="regestration" src="https://github.com/user-attachments/assets/ae3c24c3-0d7<img width="2132" height="973" alt="notes" src="https://github.com/user-attachments/assets/cd815aad-ed83-4333-b6fb-4c2bbb1a9661" />
4-46e0-b100-7238b7d29c35" />

Нотатки (/notes) — сторінка для створення та видалення текстових нотаток. Дані зберігаються у серверній сесії Flask. Підтримує додавання через кнопку або комбінацію клавіш Ctrl+Enter.
<img width="2132" height="973" alt="notes" src="https://github.com/user-attachments/assets/391e6996-d302-4fe4-b97d-4e6aad5527d2" />

Профіль (/profile) — відображає детальну інформацію про акаунт: логін, ім’я, роль та перелік дозволів, які залежать від ролі користувача (admin або user).
<img width="2151" height="1235" alt="profile" src="https://github.com/user-attachments/assets/911508ec-d84d-43b7-8ae3-a91bd043cf45" />


Спільний стан між сторінками
Спільний стан реалізований через JavaScript-об’єкт State, оголошений у базовому шаблоні base.html. Він зберігає токен авторизації, ім’я користувача та роль у localStorage браузера, що забезпечує доступ до цих даних на будь-якій сторінці застосунку без повторних запитів до сервера.

Обробка помилок
Усі запити до сервера обгорнуті у конструкцію try/catch. У разі помилки (невірний пароль, порожнє поле, збій сервера) на сторінці відображається відповідне повідомлення, яке автоматично зникає через 4 секунди. Сервер повертає відповідні HTTP-коди: 400 при некоректних даних, 401 при невірній авторизації.

​​​​​​​​​​​​​​​​
