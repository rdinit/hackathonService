from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Path, Response, status
from loguru import logger
from pydantic import BaseModel

from services.role_service import RoleService

role_service = RoleService()  # Создаём экземпляр RoleService

# Lifespan-событие
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Обработчик жизненного цикла приложения.
    Используется для инициализации данных при старте и очистки ресурсов при завершении.
    """
    logger.info("Application startup: initializing roles...")
    await role_service.init_roles()  # Инициализация ролей
    logger.info("Roles initialized successfully")
    yield  # Возвращаем управление приложению
    logger.info("Application shutdown: cleaning up...")  # Действия при завершении приложения



# Создание приложения FastAPI с lifespan
app = FastAPI(
    title="Наше первое приложение!",
    description="Прикольное приложение для генерации коротких ссылок",
    lifespan=lifespan,
)


class PutLink(BaseModel):
    link: str


def _service_link_to_real(short_link: str) -> str:
    return f"http://localhost:8000/short/{short_link}"


# @app.put("/link")
# async def put_link(put_link_request: PutLink) -> PutLink:
#     short_link = await short_link_service.put_link(put_link_request.link)
#     return PutLink(link=_service_link_to_real(short_link))
#
#
# @app.get("/short/{link}")
# async def get_link(link: str = Path(...)) -> Response:
#     real_link = await short_link_service.get_real_link(link)
#
#     if real_link is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short link not found:(")
#
#     return Response(status_code=status.HTTP_301_MOVED_PERMANENTLY, headers={"Location": real_link})

