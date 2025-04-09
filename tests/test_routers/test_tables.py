import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_session
from unittest.mock import MagicMock
from app.models.models import Table
from app.schemas.table import TableCreate


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
    mock.query.return_value.all.return_value = [
        Table(id=1, name="vip3", seats=4, location="Терраса"),
        Table(id=2, name="non_vip", seats=4, location="Холл"),
    ]
    def add_side_effect(table):
        table.id = 3
    mock.add.side_effect = add_side_effect
    return mock


@pytest.fixture
def new_table_data():
    return TableCreate(name="vip4", seats=4, location="Холл")


def test_get_tables(client: TestClient, mock_session):
    """
    Тестируем запрос на получение списка столиков.
    """
    app.dependency_overrides[get_session] = lambda: mock_session

    response = client.get("/tables")

    assert response.status_code == 200
    assert response.json()[0]["name"] == "vip3"
    assert response.json()[1]["name"] == "non_vip"


def test_create_table(client: TestClient, new_table_data, mock_session):
    """
    Тестируем создание нового столика.
    """
    app.dependency_overrides[get_session] = lambda: mock_session

    response = client.post("/tables/", json=new_table_data.model_dump())

    assert response.status_code == 201
    assert response.json()["name"] == new_table_data.name
    assert response.json()["id"] is not None

def test_create_table_error(client: TestClient, mock_session):
    """
    Тестируем создание столика с ошибкой.
    """
    # Мокируем сессию, чтобы вызвать ошибку
    mock_session.add.side_effect = Exception("Database error")

    app.dependency_overrides[get_session] = lambda: mock_session

    response = client.post("/tables", json={"name": "Test Table"})

    assert response.status_code == 422


def test_delete_table(client: TestClient, mock_session):
    """
    Тестируем удаление столика.
    """
    app.dependency_overrides[get_session] = lambda: mock_session

    response = client.delete("/tables/1")

    assert response.status_code == 200
    assert response.json() == {"message": "Столик успешно удален"}


def test_delete_table_not_found(client: TestClient, mock_session):
    """
    Тестируем удаление несуществующего столика.
    """
    mock_session.get.return_value = None

    app.dependency_overrides[get_session] = lambda: mock_session

    response = client.delete("/tables/999")

    assert response.status_code == 404


def test_delete_table_error(client: TestClient, mock_session):
    """
    Тестируем удаление столика с ошибкой.
    """
    mock_session.delete.side_effect = Exception("Delete error")

    app.dependency_overrides[get_session] = lambda: mock_session

    response = client.delete("/tables/1")

    assert response.status_code == 400
    assert "Ошибка при удалении столика" in response.json()["detail"]
