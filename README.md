# 🍽️ Restaurant Table Booking API

REST API-сервис для бронирования столиков в ресторане. 

Реализован на FastAPI, использует PostgreSQL, SQLModel и Alembic. Упакован в Docker и запускается через `docker compose`.

---

## 🚀 Быстрый старт

### 🔧 Предустановки

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### 📦 Установка и запуск

```bash
git clone https://github.com/your-username/restaurant-booking-api.git
cd AppRESTAPI
docker compose up -d
```
#### 📍 После запуска API будет доступен по адресу: http://localhost:8000/
### 🧩 Архитектура проекта
```commandline
app/
├── main.py                 # Точка входа FastAPI
├── database.py             # Подключение к БД
├── models/                 # SQLAlchemy модели
├── schemas/                # Pydantic-схемы
├── routers/                # Роутеры API
├── services/               # Логика и бизнес-правила
├── middleware/             # (опционально) логгирование и др.
├── alembic/                # Миграции Alembic
tests/
├── ...                     # Тесты (на pytest)
Dockerfile                 # Образ приложения
docker-compose.yml         # Сборка и запуск всех сервисов

```
### ⚙️ API Методы
#### 📋 Столики
* **GET /tables/** — получить список столиков
* POST **/tables/** — создать столик
* DELETE **/tables/{id}** — удалить столик

##### Пример запроса на создание:
```json
{
  "name": "Table 1",
  "seats": 4,
  "location": "Терраса"
}
```
#### 🪑 Брони
* **GET /reservations/** — получить список всех бронирований
* **POST /reservations/** — создать новое бронирование
* DELETE **/reservations/{id}** — удалить бронирование по ID

##### Пример запроса на создание:
```json
{
  "customer_name": "Иван Иванов",
  "table_id": 1,
  "reservation_time": "2025-04-09T18:00:00",
  "duration_minutes": 60
}
```
##### 🔒 Проверка конфликта: если в указанный временной промежуток столик уже занят, сервер вернёт ошибку с пояснением.

### 🛠️ Миграции
Миграции выполняются автоматически при запуске контейнера.

Ручной запуск:
```commandline
docker compose run migrate alembic upgrade head
```

### ✅ Тестирование
Тесты написаны на pytest и запускаются командой:
```commandline
pytest
```
Покрытие тестов:
```commandline
pytest --cov=app
```

### 🧠 Используемые технологии

*  **FastAPI** — быстрый веб-фреймворк  
*  **PostgreSQL** — база данных  
*  **SQLModel** — ORM  
*  **Alembic** — миграции  
*  **Docker** — контейнеризация  
*  **Pytest** — тестирование  

### 📫 Обратная связь
* По всем вопросам: EvgRf86@inbox.ru
* Репозиторий: https://github.com/MasterYodaOfficial/AppRESTAPI

##### С Уважением, Евгений.