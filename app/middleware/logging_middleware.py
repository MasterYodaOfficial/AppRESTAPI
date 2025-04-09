import logging
from fastapi import Request
import time
from typing import Any

logger = logging.getLogger(__name__)


async def log_requests(request: Request, call_next) -> Any:
    """
    Middleware для логирования входящих HTTP-запросов и ответов.

    Логирует:
    - Метод и URL запроса
    - Клиентский IP-адрес
    - Время обработки запроса
    - Статус ответа
    - Ошибки (если возникают)

    Args:
        request (Request): Входящий HTTP-запрос
        call_next (Callable): Функция для обработки запроса

    Returns:
        Response: HTTP-ответ
    """
    start_time = time.time()

    client_ip = request.client.host if request.client else "unknown"

    try:
        logger.info(
            f"Incoming request | IP: {client_ip} | "
            f"Method: {request.method} | Path: {request.url.path}"
        )

        response = await call_next(request)

        process_time = (time.time() - start_time) * 1000
        process_time_str = f"{process_time:.2f}ms"

        logger.info(
            f"Completed request | IP: {client_ip} | "
            f"Method: {request.method} | Path: {request.url.path} | "
            f"Status: {response.status_code} | Duration: {process_time_str}"
        )

        return response

    except Exception as exc:
        error_time = (time.time() - start_time) * 1000
        error_time_str = f"{error_time:.2f}ms"

        logger.error(
            f"Request failed | IP: {client_ip} | "
            f"Method: {request.method} | Path: {request.url.path} | "
            f"Error: {str(exc)} | Duration: {error_time_str}",
            exc_info=True
        )

        raise


def setup_request_logging(app) -> None:
    """
    Настраивает логирование запросов для FastAPI приложения.

    Args:
        app (FastAPI): Экземпляр FastAPI приложения

    Note:
        Добавляет middleware log_requests к приложению
    """
    app.middleware("http")(log_requests)
    logger.info("Request logging middleware successfully configured")
