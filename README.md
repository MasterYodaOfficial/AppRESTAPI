# Описание проекта AppRESTAPI
Создаем БД находясь в директории /AppRESTAPI$
```commandline
sudo docker compose up -d
```
Создаем, применяем миграцию, таблицы созданы
```commandline
alembic revision --autogenerate -m "create reservation and table models"
```
```commandline
alembic upgrade head
```

### Методы API:

#### Столики:

GET /tables/ — список всех столиков

POST /tables/ — создать новый столик

DELETE /tables/{id} — удалить столик

#### Брони:

GET /reservations/ — список всех броней

POST /reservations/ — создать новую бронь

DELETE /reservations/{id} — удалить бронь
