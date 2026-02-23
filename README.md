# dvKovalchuk

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
