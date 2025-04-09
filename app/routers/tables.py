from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.models.models import Table
from app.schemas.table import TableCreate, TableResponse
from app.database import get_session
import logging


logger = logging.getLogger(__name__)

router_tab = APIRouter(
    prefix="/tables",
    tags=["Столики"],
    responses={
        404: {"description": "Не найдено"},
        400: {"description": "Некорректный запрос"},
    },
)


@router_tab.get(
    "/",
    response_model=list[TableResponse],
    summary="Получить список всех столиков",
    description="Возвращает полный список всех столиков в ресторане",
    response_description="Список объектов столиков",
)
def get_tables(session: Session = Depends(get_session)):
    """
    Получает список всех столиков.

    Returns:
        list[TableResponse]: Список всех столиков в системе
    """
    logger.info("Запрос на получение списка столиков")
    try:
        tables = session.query(Table).all()
        logger.info(f"Успешно получено {len(tables)} столиков")
        return tables
    except Exception as e:
        logger.error(f"Ошибка при получении столиков: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка при получении столиков: {str(e)}")


@router_tab.post(
    "/",
    response_model=TableResponse,
    status_code=201,
    summary="Создать новый столик",
    description="Создает новую запись о столике в ресторане",
    response_description="Созданный столик",
    responses={
        201: {"description": "Столик успешно создан"},
    },
)
def create_table(table: TableCreate, session: Session = Depends(get_session)):
    """
    Создает новый столик.

    Args:
        table (TableCreate): Данные для создания столика
        session (Session): Сессия базы данных

    Returns:
        TableResponse: Созданный столик
    """
    logger.info(f"Запрос на создание столика: {table.dict()}")

    try:
        db_table = Table(**table.dict())
        session.add(db_table)
        session.commit()
        session.refresh(db_table)
        logger.info(f"Столик создан: ID {db_table.id} - {db_table.name}")
        return db_table
    except Exception as e:
        session.rollback()
        logger.error(f"Ошибка при создании столика: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Ошибка при создании столика: {str(e)}")


@router_tab.delete(
    "/{table_id}",
    summary="Удалить столик",
    description="Удаляет столик по указанному ID",
    response_description="Сообщение об успешном удалении",
    responses={
        200: {"description": "Столик удален"},
        404: {"description": "Столик не найден"},
    },
)
def delete_table(table_id: int, session: Session = Depends(get_session)):
    """
    Удаляет столик по ID.

    Args:
        table_id (int): ID столика для удаления
        session (Session): Сессия базы данных

    Returns:
        dict: Сообщение об успешном удалении

    Raises:
        HTTPException: 404 если столик не найден
    """
    logger.info(f"Запрос на удаление столика ID {table_id}")

    table = session.get(Table, table_id)
    if not table:
        logger.warning(f"Столик {table_id} не найден")
        raise HTTPException(status_code=404, detail=f"Столик {table_id} не найден")

    try:
        session.delete(table)
        session.commit()
        logger.info(f"Столик {table_id} успешно удален")
        return {"message": "Столик успешно удален"}
    except Exception as e:
        session.rollback()
        logger.error(f"Ошибка при удалении столика {table_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Ошибка при удалении столика {table_id}: {str(e)}")
