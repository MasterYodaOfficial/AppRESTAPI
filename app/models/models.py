from datetime import datetime
from sqlmodel import SQLModel, Field, Column, DateTime
from sqlalchemy.dialects.postgresql import ExcludeConstraint
from sqlalchemy import text
from typing import Optional

class Table(SQLModel, table=True):
    """
    Модель, представляющая столик в ресторане.

    Атрибуты:
        id (int, optional): Уникальный идентификатор столика (генерируется автоматически).
        Name (str): Название или номер столика.
        Seats (int): Количество посадочных мест (должно быть больше 0).
        Location (str): Расположение столика в ресторане (например, "зал", "трасса", "VIP").
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    seats: int = Field(gt=0, description="Количество мест должно быть больше 0")
    location: str


class Reservation(SQLModel, table=True):
    """
    Модель, представляющая бронирование столика клиентом.

    Атрибуты:
        id (int, optional): Уникальный идентификатор бронирования.
        Customer_name (str): Имя клиента, сделавшего бронирование.
        Table_id (int): ID столика, на который делается бронирование.
        Reservation_time (datetime): Дата и время начала бронирования.
        Duration_minutes (int): Длительность бронирования в минутах (должна быть больше 0).

    Ограничения:
        - Исключающее ограничение не допускает пересечений бронирований по времени для одного и того же столика.
          Это реализовано через PostgreSQL ExcludeConstraint с использованием диапазона времени.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_name: str
    table_id: int = Field(foreign_key="table.id")
    reservation_time: datetime = Field(
        sa_column=Column(DateTime()),
        description="Начало бронирования"
    )
    duration_minutes: int = Field(gt=0, description="Длительность должна быть больше 0 минут")

    __table_args__ = (
        ExcludeConstraint(
            ('table_id', '='),
            (
                text("tsrange(reservation_time, reservation_time + duration_minutes * interval '1 minute')"),
                '&&'
            ),
            name="no_overlapping_reservations"
        ),
    )
