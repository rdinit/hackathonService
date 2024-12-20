from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from uuid import UUID
from loguru import logger

from persistent.db.team import Team
from services.team_service import TeamService
from services.hacker_service import HackerService

team_service = TeamService()

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
    hacker_ids: List[UUID]


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
        logger.exception("Ошибка при получении списка команд.")
        raise HTTPException(status_code=400, detail="Не удалось получить список команд.")


@team_router.post("/", response_model=CreateTeamPostResponse, status_code=201)
async def create(team_request: TeamCreatePostRequest):
    """
    Создать новую команду.
    """
    logger.info(f"Попытка создания команды: {team_request.name} с владельцем {team_request.ownerID}.")
    try:
        team_id = await team_service.create_team(team_request.ownerID, team_request.name, team_request.size)
        logger.info(f"Команда успешно создана с ID: {team_id}.")
        return CreateTeamPostResponse(id=team_id)
    except Exception as e:
        logger.exception("Ошибка при создании команды.")
        raise HTTPException(status_code=400, detail="Не удалось создать команду.")


@team_router.post("/add/", response_model=GetTeamByIdGetResponse, status_code=201)
async def add_hacker_to_team(team_request: AddHackerToTeamRequest):
    """
    Добавить участника в команду по ID.
    """
    logger.info(f"Попытка добавить хакера {team_request.hacker_id} в команду {team_request.team_id}.")
    try:
        team = await team_service.get_team_by_id(team_request.team_id)
        if not team:
            logger.warning(f"Команда с ID {team_request.team_id} не найдена.")
            raise HTTPException(status_code=404, detail="Команда не найдена")

        hacker = await HackerService().get_hacker_by_id(team_request.hacker_id)
        if not hacker:
            logger.warning(f"Хакер с ID {team_request.hacker_id} не найден.")
            raise HTTPException(status_code=404, detail="Хакер не найден")

        await team_service.add_hacker_to_team(team_request.team_id, team_request.hacker_id)
        logger.info(f"Хакер {team_request.hacker_id} успешно добавлен в команду {team_request.team_id}.")

        return GetTeamByIdGetResponse(
            id=team.id,
            ownerID=team.owner_id,
            name=team.name,
            size=team.size,
            hacker_ids=[hacker.id for hacker in team.hackers],
        )
    except Exception as e:
        logger.exception("Ошибка при добавлении хакера в команду.")
        raise HTTPException(status_code=400, detail="Не удалось добавить хакера в команду.")


@team_router.get("/{team_id}", response_model=GetTeamByIdGetResponse)
async def get_by_id(team_id: UUID):
    """
    Получить информацию о команде по её ID.
    """
    logger.info(f"Запрос информации о команде с ID {team_id}.")
    try:
        team = await team_service.get_team_by_id(team_id)
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
