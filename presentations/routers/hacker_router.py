from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from uuid import UUID

from persistent.db.role import Role
from persistent.db.team import Team
from services.hacker_service import HackerService

hacker_service = HackerService()  # Создаём экземпляр RoleService

hacker_router = APIRouter(
    prefix="/hacker",
    tags=["Hackers"],
    responses={404: {"description": "Not Found"}},
)


class HackerDto(BaseModel):
    user_id: UUID
    name: str
    roles: List[str]
    team_ids: List[UUID]


class HackerGetAllResponse(BaseModel):
    hackers: List[HackerDto]


class HackerCreatePostRequest(BaseModel):
    user_id: UUID
    name: str


class CreateHackerPostResponse(BaseModel):
    id: UUID


class GetHackerByIdGetRequest(BaseModel):
    hacker_id: UUID


class GetHackerByIdGetResponse(BaseModel):
    user_id: UUID
    name: str
    roles: List[str]
    team_ids: List[UUID]


@hacker_router.get("/", response_model=HackerGetAllResponse)
async def get_all():
    """
    Get all hackers.

    Returns hackers' information including assigned roles.
    """
    try:
        hackers = await hacker_service.get_all_hackers()

        return HackerGetAllResponse(
            hackers=[
                HackerDto(id=hacker.id,
                          user_id=hacker.user_id,
                          name=hacker.name,
                          roles=[role.name for role in hacker.roles],
                          team_ids=[team.id for team in hacker.teams],)
                for hacker in hackers
            ]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail="Чёто хз не работает чё1т :(")


@hacker_router.post("/", response_model=CreateHackerPostResponse, status_code=201)
async def create(hacker_request: HackerCreatePostRequest):
    """
    Create a new hacker.

    - **user_id**: Unique identifier of the user.
    - **name**: Name of the hacker.

    Returns the created hacker with assigned roles.
    """
    try:
        hacker_id = await hacker_service.create_hacker(hacker_request.user_id, hacker_request.name)
        return CreateHackerPostResponse(
            id=hacker_id,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail="Хакер с таким user_id уже есть")


@hacker_router.get("/{hacker_id}", response_model=GetHackerByIdGetResponse)
async def get_by_id(hacker_id: UUID):
    """
    Get details of a hacker by their ID.

    - **hacker_id**: Unique identifier of the hacker.

    Returns hacker information including assigned roles.
    """
    try:
        hacker = await hacker_service.get_hacker_by_id(hacker_id)
        if not hacker:
            raise HTTPException(status_code=404, detail="Хакер не найден")

        return GetHackerByIdGetResponse(
            id=hacker.id,
            user_id=hacker.user_id,
            name=hacker.name,
            roles=[role.name for role in hacker.roles],
            team_ids=[team.id for team in hacker.teams],
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
