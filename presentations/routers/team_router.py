from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from uuid import UUID
from loguru import logger

from persistent.db.team import Team
from services.team_service import TeamService
from services.hacker_service import HackerService

team_service = TeamService()  # Создаём экземпляр TeamService

team_router = APIRouter(
    prefix="/team",
    tags=["Teams"],
    responses={404: {"description": "Not Found"}},
)


class TeamDto(BaseModel):
    id: UUID
    ownerID: UUID
    name: str
    size: int
    hacker_ids: List[UUID]  # Список ID хакеров, состоящих в команде


class TeamGetAllResponse(BaseModel):
    teams: List[TeamDto]


class TeamCreatePostRequest(BaseModel):
    ownerID: UUID
    name: str
    size: int


class CreateTeamPostResponse(BaseModel):
    id: UUID


class AddHackerToTeamRequest(BaseModel):
    team_id: UUID
    hacker_id: UUID


class AddHackerToTeamResponse(BaseModel):
    id: UUID
    ownerID: UUID
    name: str
    size: int
    hacker_ids: List[UUID]  # Список ID хакеров в команде


class GetTeamByIdGetRequest(BaseModel):
    team_id: UUID


class GetTeamByIdGetResponse(BaseModel):
    id: UUID
    ownerID: UUID
    name: str
    size: int
    hacker_ids: List[UUID]


@team_router.get("/", response_model=TeamGetAllResponse)
async def get_all():
    """
    Получить список всех команд.

    Возвращает информацию обо всех командах и их хакерах.
    """
    logger.info("Получение списка всех команд.")
    try:
        teams = await team_service.get_all_teams()
        logger.info(f"Успешно получено {len(teams)} команд.")
        return TeamGetAllResponse(
            teams=[
                TeamDto(
                    id=team.id,
                    ownerID=team.owner_id,
                    name=team.name,
                    size=team.size,
                    hacker_ids=[hacker.id for hacker in team.hackers],
                )
                for team in teams
            ]
        )
    except Exception as e:
        logger.exception(f"Ошибка при получении списка команд. {str(e)}")
        raise HTTPException(status_code=400, detail="Не удалось получить список команд.")


@team_router.post("/", response_model=CreateTeamPostResponse, status_code=201)
async def create(request: TeamCreatePostRequest):
    """
    Создать новую команду.

    - **ownerID**: Идентификатор создателя команды.
    - **name**: Название команды.
    - **size**: Размер команды..

    Возвращает идентификатор созданной команды.
    """
    logger.info(f"Попытка создания команды: {request.name} с владельцем {request.ownerID}.")
    try:
        team_id = await team_service.create_team(request.ownerID, request.name, request.size)
        logger.info(f"Команда успешно создана с ID: {team_id}.")
        return CreateTeamPostResponse(id=team_id)
    except Exception as e:
        logger.exception(f"Ошибка при создании команды {str(e)}.")
        raise HTTPException(status_code=400, detail="Не удалось создать команду.")


@team_router.post("/add_hacker", response_model=AddHackerToTeamResponse, status_code=201)
async def add_hacker_to_team(request: AddHackerToTeamRequest):
    """
    Добавить участника в команду по ID.

    - **team_id**: Уникальный идентификатор команды.
    - **hacker_id**: Уникальный идентификатор хакера, которого нужно добавить в команду.

    Возвращает информацию о команде после добавления участника.
    """
    logger.info(f"Попытка добавить хакера {request.hacker_id} в команду {request.team_id}.")
    try:
        # Добавляем хакера в команду
        team = await team_service.add_hacker_to_team(request.team_id, request.hacker_id)

        # Возвращаем обновленную информацию о команде
        return AddHackerToTeamResponse(
            id=team.id,
            ownerID=team.owner_id,
            name=team.name,
            size=team.size,
            hacker_ids=[hacker.id for hacker in team.hackers],
        )
    except Exception as e:
        logger.exception(f"Adding hacker to team: {str(e)}")
        raise HTTPException(status_code=400, detail="Не удалось добавить хакера")


@team_router.get("/{team_id}", response_model=GetTeamByIdGetResponse)
async def get_by_id(request: GetTeamByIdGetRequest):
    """
    Получить информацию о команде по её ID.

    - **team_id**: Уникальный идентификатор команды.
    - **ownerID**: Идентификатор создателя команды.

    Возвращает информацию о команде и её хакерах.
    """
    logger.info(f"Запрос информации о команде с ID {team_id}.")
    try:
        team = await team_service.get_team_by_id(request.team_id)
        if not team:
            logger.warning(f"Команда с ID {team_id} не найдена.")
            raise HTTPException(status_code=404, detail="Команда не найдена")

        logger.info(f"Команда с ID {team_id} найдена.")
        return GetTeamByIdGetResponse(
            id=team.id,
            ownerID=team.owner_id,
            name=team.name,
            size=team.size,
            hacker_ids=[hacker.id for hacker in team.hackers],
        )
    except Exception as e:
        logger.exception(f"Ошибка при получении информации о команде с ID {team_id}.")
        raise HTTPException(status_code=400, detail=str(e))
