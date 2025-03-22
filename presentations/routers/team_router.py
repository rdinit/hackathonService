import uuid
from typing import List

from fastapi import APIRouter, HTTPException, status
from loguru import logger
from pydantic import BaseModel
from uuid import UUID

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
    max_size: int
    hacker_ids: List[UUID]  # Список ID хакеров, состоящих в команде


class TeamGetAllResponse(BaseModel):
    teams: List[TeamDto]


class TeamCreatePostRequest(BaseModel):
    ownerID: UUID
    name: str
    max_size: int


class CreateTeamPostResponse(BaseModel):
    id: UUID


class AddHackerToTeamRequest(BaseModel):
    team_id: UUID
    hacker_id: UUID


class AddHackerToTeamResponse(BaseModel):
    id: UUID
    ownerID: UUID
    name: str
    max_size: int
    hacker_ids: List[UUID]


class GetTeamByIdGetResponse(BaseModel):
    id: UUID
    ownerID: UUID
    name: str
    max_size: int
    hacker_ids: List[UUID]


@team_router.get("/", response_model=TeamGetAllResponse)
async def get_all():
    """
    Получить список всех команд.
    """
    logger.info("team_get_all")
    teams = await team_service.get_all_teams()

    return TeamGetAllResponse(
        teams=[
            TeamDto(
                id=team.id,
                ownerID=team.owner_id,
                name=team.name,
                max_size=team.max_size,
                hacker_ids=[hacker.id for hacker in team.hackers],
            )
            for team in teams
        ]
    )


@team_router.post("/", response_model=CreateTeamPostResponse, status_code=201)
async def create(request: TeamCreatePostRequest):
    """
    Создать команду.
    """
    logger.info(f"team_create: {request.name}")
    team_id, status_code = await team_service.create_team(request.ownerID, request.name, request.max_size)

    if status_code == -1:
        logger.error(f"team_create: invalid max_size {request.max_size}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="max_size должен быть больше 0")
    if status_code == -2:
        logger.error(f"team_create: team already exists")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Команда с таким владельцем и названием уже существует")

    return CreateTeamPostResponse(
        id=team_id,
    )


@team_router.post("/add_hacker", response_model=AddHackerToTeamResponse, status_code=201)
async def add_hacker_to_team(request: AddHackerToTeamRequest):
    """
    Добавить участника в команду по ID.
    """
    logger.info(f"team_add_hacker: {request.team_id} {request.hacker_id}")
    team, status_code = await team_service.add_hacker_to_team(request.team_id, request.hacker_id)
    
    if status_code == -1:
        logger.error(f"team_add_hacker: team {request.team_id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Команда не найдена")
    if status_code == -2:
        logger.error(f"team_add_hacker: hacker {request.hacker_id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Хакер не найден")
    if status_code == -3:
        logger.error(f"team_add_hacker: team {request.team_id} is full")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Команда заполнена")
    if status_code == -4:
        logger.error(f"team_add_hacker: hacker {request.hacker_id} already in team")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Хакер уже в команде")
    if status_code < 0:
        logger.error(f"team_add_hacker: unknown error {status_code}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось добавить хакера")

    return AddHackerToTeamResponse(
        id=team.id,
        ownerID=team.owner_id,
        name=team.name,
        max_size=team.max_size,
        hacker_ids=[hacker.id for hacker in team.hackers],
    )


@team_router.get("/{team_id}", response_model=GetTeamByIdGetResponse)
async def get_by_id(team_id: UUID):
    """
    Получить информацию о команде по её ID.
    """
    logger.info(f"team_get_by_id: {team_id}")
    team, found = await team_service.get_team_by_id(team_id)

    if not found:
        logger.error(f"team_get_by_id: {team_id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Команда не найдена")

    return GetTeamByIdGetResponse(
        id=team.id,
        ownerID=team.owner_id,
        name=team.name,
        max_size=team.max_size,
        hacker_ids=[hacker.id for hacker in team.hackers],
    )
