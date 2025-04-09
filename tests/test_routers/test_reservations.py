import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_session
from unittest.mock import MagicMock
from app.models.models import Reservation
from app.schemas.reservation import ReservationCreate
import datetime


@pytest.fixture
def client():
    """
    Фикстура для тестирования клиента FastAPI.
    """
    client = TestClient(app)
    return client


@pytest.fixture
def mock_session():
    """
    Мок-сессия для тестирования базы данных.
    """
    mock = MagicMock()

    # Мокируем данные для таблиц и бронирований
    mock.query.return_value.all.return_value = [
        Reservation(id=1, table_id=1, reservation_time="2025-04-10T12:00:00", duration_minutes=60, customer_name="alesha"),
        Reservation(id=2, table_id=2, reservation_time="2025-04-10T14:00:00", duration_minutes=90, customer_name="alesha2")
    ]
    return mock


@pytest.fixture
def new_reservation_data():
    reservation_time = datetime.datetime(2025, 4, 10, 16, 0).isoformat()
    return ReservationCreate(table_id=1, reservation_time=reservation_time,
                             duration_minutes=60, customer_name='test_name')


def test_get_reservations(client: TestClient, mock_session):
    """
    Тестируем запрос на получение списка бронирований.
    """
    app.dependency_overrides[get_session] = lambda: mock_session

    response = client.get("/reservations")

    assert response.status_code == 200
    assert response.json()[0]["reservation_time"] == "2025-04-10T12:00:00"
    assert response.json()[1]["reservation_time"] == "2025-04-10T14:00:00"


def test_create_reservation_conflict(client: TestClient, mock_session):
    """
    Тестируем создание бронирования с конфликтом времени.
    """
    mock_session.query.return_value.filter.return_value.first.return_value = Reservation(id=1,
                                                                                         table_id=1,
                                                                                         reservation_time="2025-04-10T12:00:00",
                                                                                         duration_minutes=60)

    app.dependency_overrides[get_session] = lambda: mock_session

    response = client.post("/reservations", json={"table_id": 1, "reservation_time": "2025-04-10T12:30:00", "duration_minutes": 60})

    assert response.status_code == 422


def test_delete_reservation(client: TestClient, mock_session):
    """
    Тестируем удаление бронирования.
    """
    app.dependency_overrides[get_session] = lambda: mock_session

    response = client.delete("/reservations/1")

    assert response.status_code == 200
    assert response.json() == {"message": "Бронирование успешно удалено"}


def test_delete_reservation_not_found(client: TestClient, mock_session):
    """
    Тестируем удаление несуществующего бронирования.
    """
    mock_session.get.return_value = None

    app.dependency_overrides[get_session] = lambda: mock_session

    response = client.delete("/reservations/999")

    assert response.status_code == 404


def test_delete_reservation_error(client: TestClient, mock_session):
    """
    Тестируем удаление бронирования с ошибкой.
    """
    mock_session.delete.side_effect = Exception("Delete error")

    app.dependency_overrides[get_session] = lambda: mock_session

    response = client.delete("/reservations/1")

    assert response.status_code == 500
