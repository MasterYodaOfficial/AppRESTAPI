from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
import logging
from app.logging_config import setup_logging
from app.routers.tables import router_tab
from app.routers.reservations import router_res


setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(appi: FastAPI):
    _ = appi
    logger.info("Запуск приложения...")
    yield
    logger.info("Завершение работы приложения...")


app = FastAPI(lifespan=lifespan)
app.include_router(router_res)
app.include_router(router_tab)


@app.get("/", response_class=HTMLResponse)
def read_root():
    logger.info("Accessed root endpoint")
    return """
    <html>
        <head><title>Restaurant Booking API</title></head>
        <body>
            <h1>Добро пожаловать в API для бронирования столиков!</h1>
        </body>
    </html>
    """


if __name__ == "__main__":
    logger.info("Starting server...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_config=None,
    )
