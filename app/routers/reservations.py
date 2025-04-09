from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.models.models import Reservation, Table
from app.schemas.reservation import ReservationCreate, ReservationResponse
from app.database import get_session
from app.services.reservation import check_reservation_conflict
import logging


logger = logging.getLogger(__name__)

router_res = APIRouter(
    prefix="/reservations",
    tags=["Бронирования"],
    responses={
        404: {"description": "Не найдено"},
        400: {"description": "Некорректный запрос"},
    },
)


@router_res.get(
    "/",
    response_model=list[ReservationResponse],
    summary="Получить список всех бронирований",
    description="Возвращает полный список всех бронирований в системе",
    response_description="Список объектов бронирований",
)
def get_reservations(session: Session = Depends(get_session)):
    """
    Получает список всех бронирований.

    Returns:
        list[ReservationResponse]: Список всех бронирований в системе
    """
    logger.info("Запрос на получение списка бронирований")
    try:
        reservations = session.query(Reservation).all()
        logger.info(f"Успешно получено {len(reservations)} бронирований")
        return reservations
    except Exception as e:
        logger.error(f"Ошибка при получении бронирований: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка при получении бронирований: {str(e)}")


@router_res.post(
    "/",
    response_model=ReservationResponse,
    status_code=201,
    summary="Создать новое бронирование",
    description="Создает новое бронирование с проверкой доступности столика",
    response_description="Созданное бронирование",
    responses={
        201: {"description": "Бронирование успешно создано"},
        404: {"description": "Столик не найден"},
        400: {"description": "Конфликт временного слота"},
    },
)
def create_reservation(
        reservation: ReservationCreate,
        session: Session = Depends(get_session)
):
    """
    Создает новое бронирование.

    Args:
        reservation (ReservationCreate): Данные для создания бронирования
        session (Session): Сессия базы данных

    Returns:
        ReservationResponse: Созданное бронирование

    Raises:
        HTTPException: 404 если столик не найден
        HTTPException: 400 если временной слот занят
    """
    logger.info(
        f"Запрос на создание бронирования: {reservation.dict()}"
    )

    table = session.get(Table, reservation.table_id)
    if not table:
        logger.warning(f"Столик {reservation.table_id} не найден")
        raise HTTPException(status_code=404, detail=f"Столик {reservation.table_id} не найден")

    if check_reservation_conflict(
            session,
            reservation.table_id,
            reservation.reservation_time,
            reservation.duration_minutes
    ):
        logger.warning(
            f"Конфликт времени для столика {reservation.table_id} "
            f"на {reservation.reservation_time}"
        )
        raise HTTPException(status_code=400, detail="Временной слот занят")

    try:
        # Тут серриализацию явную добавил, чтобы наверника
        reservation_dict = reservation.dict()
        reservation_dict['reservation_time'] = reservation_dict['reservation_time'].isoformat()
        db_reservation = Reservation(**reservation.dict())
        session.add(db_reservation)
        session.commit()
        session.refresh(db_reservation)
        logger.info(f"Бронирование создано: ID {db_reservation.id}")
        return db_reservation
    except Exception as e:
        session.rollback()
        logger.error(f"Ошибка при создании бронирования: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка при создании бронирования: {str(e)}")


@router_res.delete(
    "/{reservation_id}",
    summary="Удалить бронирование",
    description="Удаляет бронирование по указанному ID",
    response_description="Сообщение об успешном удалении",
    responses={
        200: {"description": "Бронирование удалено"},
        404: {"description": "Бронирование не найдено"},
    },
)
def delete_reservation(
        reservation_id: int,
        session: Session = Depends(get_session)
):
    """
    Удаляет бронирование по ID.

    Args:
        reservation_id (int): ID бронирования для удаления
        session (Session): Сессия базы данных

    Returns:
        dict: Сообщение об успешном удалении

    Raises:
        HTTPException: 404 если бронирование не найдено
    """
    logger.info(f"Запрос на удаление бронирования ID {reservation_id}")

    reservation = session.get(Reservation, reservation_id)
    if not reservation:
        logger.warning(f"Бронирование {reservation_id} не найдено")
        raise HTTPException(status_code=404, detail=f"Бронирование {reservation_id} не найдено")

    try:
        session.delete(reservation)
        session.commit()
        logger.info(f"Бронирование {reservation_id} успешно удалено")
        return {"message": "Бронирование успешно удалено"}
    except Exception as e:
        session.rollback()
        logger.error(f"Ошибка при удалении бронирования {reservation_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении бронирования {reservation_id}: {str(e)}")
