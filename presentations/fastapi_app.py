from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Path, Response, status
from loguru import logger
from pydantic import BaseModel

from services.hacker_service import HackerService
from services.role_service import RoleService

role_service = RoleService()  # Создаём экземпляр RoleService
hacker_service = HackerService()  # Создаём экземпляр RoleService

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

    all_roles = await role_service.get_all_roles()  # Получаем все роли
    # Проверка инициализации ролей
    logger.info(f"Roles in system: {all_roles}")
    for role in all_roles:
        logger.info(
            f"Role: {role.name}")

    # Создаем хакера
    user_id = uuid4()  # Уникальный идентификатор пользователя
    hacker_id = await hacker_service.create_hacker(user_id, "John Doe")
    # Выводим всех хакеров
    all_hackers = await hacker_service.get_all_hackers()  # Получаем всех хакеров
    logger.info("All hackers in the system:")
    for hacker in all_hackers:
        logger.info(f"Hacker ID: {hacker.id}, Name: {hacker.name}, User UUID: {hacker.user_id}, Roles: {hacker.roles}")

    # Добавляем роли хакеру
    await hacker_service.add_roles_to_hacker(hacker_id, all_roles[:2])
    # Выводим всех хакеров
    all_hackers = await hacker_service.get_all_hackers()  # Получаем всех хакеров
    logger.info("All hackers in the system:")
    for hacker in all_hackers:
        logger.info(f"Hacker ID: {hacker.id}, Name: {hacker.name}, User UUID: {hacker.user_id}, Roles: {hacker.roles}")

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

