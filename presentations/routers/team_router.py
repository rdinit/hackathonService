from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from uuid import UUID

from persistent.db.team import Team
from presentations.fastapi_app import hacker_service
from services.team_service import TeamService

team_service = TeamService()  # Создаём экземпляр TeamService

team_router = APIRouter(
    prefix="/team",
    tags=["Teams"],
    responses={404: {"size": "Not Found"}},
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


class GetTeamByIdGetResponse(BaseModel):
    id: UUID
    ownerID: UUID
    name: str
    size: int
    hacker_ids: List[UUID]  # Список ID хакеров в команде


@team_router.get("/", response_model=TeamGetAllResponse)
async def get_all():
    """
    Получить список всех команд.

    Возвращает информацию обо всех командах и их хакерах.
    """
    try:
        teams = await team_service.get_all_teams()

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
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail="Не удалось получить список команд.")


@team_router.post("/", response_model=CreateTeamPostResponse, status_code=201)
async def create(team_request: TeamCreatePostRequest):
    """
    Создать новую команду.

    - **ownerID**: Идентификатор создателя команды.
    - **name**: Название команды.
    - **size**: Размер команды..

    Возвращает идентификатор созданной команды.
    """
    try:
        team_id = await team_service.create_team(team_request.ownerID, team_request.name, team_request.size)
        return CreateTeamPostResponse(
            id=team_id,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail="Не удалось создать команду.")


@team_router.post("/", response_model=GetTeamByIdGetResponse, status_code=201)
async def add_hacker_to_team(team_request: AddHackerToTeamRequest):
    """
    Добавить участника в команду по ID.

    - **team_id**: Уникальный идентификатор команды.
    - **hacker_id**: Уникальный идентификатор хакера, которого нужно добавить в команду.

    Возвращает информацию о команде после добавления участника.
    """
    try:
        # Проверяем, существует ли команда и хакер
        team = await team_service.get_team_by_id(team_request.team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Команда не найдена")

        hacker = await hacker_service.get_hacker_by_id(team_request.hacker_id)
        if not hacker:
            raise HTTPException(status_code=404, detail="Хакер не найден")

        # Добавляем хакера в команду
        await team_service.add_hacker_to_team(team_request.team_id, team_request.hacker_id)

        # Возвращаем обновленную информацию о команде
        return GetTeamByIdGetResponse(
            id=team.id,
            ownerID=team.owner_id,
            name=team.name,
            size=team.size,
            hacker_ids=[hacker.id for hacker in team.hackers],
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail="Не удалось добавить хакера в команду.")


@team_router.get("/{team_id}", response_model=GetTeamByIdGetResponse)
async def get_by_id(team_id: UUID):
    """
    Получить информацию о команде по её ID.

    - **team_id**: Уникальный идентификатор команды.
    - **ownerID**: Идентификатор создателя команды.

    Возвращает информацию о команде и её хакерах.
    """
    try:
        team = await team_service.get_team_by_id(team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Команда не найдена")

        return GetTeamByIdGetResponse(
            id=team.id,
            ownerID=team.owner_id,
            name=team.name,
            size=team.size,
            hacker_ids=[hacker.id for hacker in team.hackers],
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
