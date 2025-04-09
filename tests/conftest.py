import pytest
from sqlmodel import SQLModel, create_engine, Session
from app.models.models import Table, Reservation

DATABASE_URL = "postgresql+psycopg2://user_test:password_test@localhost/db_test"

engine = create_engine(DATABASE_URL, echo=True)

@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
