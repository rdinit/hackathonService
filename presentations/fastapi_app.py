from contextlib import asynccontextmanager
from datetime import datetime
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Path, Response, status
from loguru import logger
from pydantic import BaseModel

from presentations.routers.hacker_router import hacker_router
from services.hacker_service import HackerService
from services.role_service import RoleService
from services.team_service import TeamService
from services.hackathon_service import HackathonService
from services.winner_solution_service import WinnerSolutionService

role_service = RoleService()  # Создаём экземпляр RoleService
hacker_service = HackerService()  # Создаём экземпляр RoleService

# Lifespan-событие
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Обработчик жизненного цикла приложения.
    Используется для инициализации данных при старте и очистки ресурсов при завершении.
    """
    all_roles = await role_service.get_all_roles()  # Получаем все роли
    if len(all_roles) == 0:
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

        # Добавляем роли хакеру
        await hacker_service.add_roles_to_hacker(hacker_id, all_roles[:2])

        # Создаем команду и добавляем хакера
        team_service = TeamService()
        team_name = "Elite Hackers"
        team_size = 5
        try:
            team_id = await team_service.create_team(owner_id=hacker_id, name=team_name, size=team_size)
            logger.info(f"Team '{team_name}' created with ID: {team_id}")
        except ValueError as e:
            logger.error(f"Error creating team: {e}")
            team_id = None

        if team_id:
            try:
                await team_service.add_hacker_to_team(team_id, hacker_id)
                logger.info(f"Hacker with ID '{hacker_id}' added to team '{team_name}'.")
            except ValueError as e:
                logger.error(f"Error adding hacker to team: {e}")

        # Создаем хакатон
        hackathon_service = HackathonService()
        hackathon_name = "Global Hackathon 2024"
        task_description = "Solve real-world problems with innovative solutions."
        start_of_registration = datetime.strptime("2024-01-01T09:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
        end_of_registration = datetime.strptime("2024-01-15T23:59:59Z", "%Y-%m-%dT%H:%M:%SZ")
        start_of_hack = datetime.strptime("2024-01-20T09:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
        end_of_hack = datetime.strptime("2024-01-21T18:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
        amount_money = 10000.0
        hack_type = "offline"  # Используем корректное значение: "online" или "offline"

        try:
            hackathon_id = await hackathon_service.create_hackathon(
                name=hackathon_name,
                task_description=task_description,
                start_of_registration=start_of_registration,
                end_of_registration=end_of_registration,
                start_of_hack=start_of_hack,
                end_of_hack=end_of_hack,
                amount_money=amount_money,
                hack_type=hack_type,
            )
            logger.info(f"Hackathon '{hackathon_name}' created with ID: {hackathon_id}")
        except Exception as e:
            logger.error(f"Error creating hackathon: {e}")

        # Создаем решение хакатона
        if hackathon_id:
            winner_solution_service = WinnerSolutionService()
            link_to_solution = "https://github.com/team/solution"
            link_to_presentation = "https://slides.com/team/presentation"
            win_money = 5000.0  # Призовые деньги
            can_share = True  # Решение доступно для публикации

            try:
                solution_id = await winner_solution_service.create_winner_solution(
                    hackathon_id=hackathon_id,
                    team_id=team_id,
                    win_money=win_money,
                    link_to_solution=link_to_solution,
                    link_to_presentation=link_to_presentation,
                    can_share=can_share,
                )
                logger.info(f"Winner solution created with ID: {solution_id}")
            except Exception as e:
                logger.error(f"Error creating winner solution: {e}")

    yield  # Возвращаем управление приложению

    logger.info("Application shutdown: cleaning up...")  # Действия при завершении приложения




# Создание приложения FastAPI с lifespan
app = FastAPI(
    title="Наше первое приложение!",
    description="Прикольное приложение для генерации коротких ссылок",
    lifespan=lifespan,
)

app.include_router(hacker_router)

