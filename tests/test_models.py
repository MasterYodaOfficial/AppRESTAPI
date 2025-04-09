from datetime import datetime, timedelta
from sqlmodel import Session
from app.models.models import Table, Reservation
import pytest
from sqlalchemy.exc import IntegrityError

def test_create_table(session: Session):
    """Тест создания таблицы"""
    table = Table(name="A1", seats=4, location="Main Hall")
    session.add(table)
    session.commit()
    assert table.id is not None

def test_create_reservation(session: Session):
    """Тест создания бронирования"""
    table = Table(name="B1", seats=2, location="Patio")
    session.add(table)
    session.commit()

    reservation = Reservation(
        customer_name="John Doe",
        table_id=table.id,
        reservation_time=datetime.now(),
        duration_minutes=60
    )
    session.add(reservation)
    session.commit()
    assert reservation.id is not None

def test_overlap_reservations_fail(session: Session):
    """Проверка бронирования при пересекающегося времени"""
    table = Table(name="C1", seats=2, location="VIP")
    session.add(table)
    session.commit()

    now = datetime.now()
    res1 = Reservation(
        customer_name="Alice",
        table_id=table.id,
        reservation_time=now,
        duration_minutes=60
    )
    session.add(res1)
    session.commit()

    # Попытка пересекающегося бронирования
    res2 = Reservation(
        customer_name="Bob",
        table_id=table.id,
        reservation_time=now + timedelta(minutes=30),
        duration_minutes=60
    )
    session.add(res2)
    with pytest.raises(IntegrityError):
        session.commit()
