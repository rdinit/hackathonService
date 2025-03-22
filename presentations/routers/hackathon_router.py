from datetime import datetime
from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from loguru import logger

from services.hackathon_service import HackathonService

hackathon_service = HackathonService()

hackathon_router = APIRouter(
    prefix="/hackathon",
    tags=["Hackathons"],
    responses={404: {"description": "Not Found"}},
)


class HackathonDto(BaseModel):
    id: UUID
    name: str
    task_description: str
    start_of_registration: datetime
    end_of_registration: datetime
    start_of_hack: datetime
    end_of_hack: datetime
    amount_money: float
    type: str


class HackathonGetAllResponse(BaseModel):
    hackathons: List[HackathonDto]


class HackathonCreatePostRequest(BaseModel):
    name: str
    task_description: str
    start_of_registration: datetime
    end_of_registration: datetime
    start_of_hack: datetime
    end_of_hack: datetime
    amount_money: float
    type: str


class HackathonCreatePostResponse(BaseModel):
    id: UUID


class HackathonGetByIdResponse(BaseModel):
    id: UUID
    name: str
    task_description: str
    start_of_registration: datetime
    end_of_registration: datetime
    start_of_hack: datetime
    end_of_hack: datetime
    amount_money: float
    type: str


@hackathon_router.get("/", response_model=HackathonGetAllResponse)
async def get_all_hackathons():
    """
    Получить список всех хакатонов.
    """
    logger.info("hackathon_get_all")
    hackathons = await hackathon_service.get_all_hackathons()

    return HackathonGetAllResponse(
        hackathons=[
            HackathonDto(
                id=hackathon.id,
                name=hackathon.name,
                task_description=hackathon.task_description,
                start_of_registration=hackathon.start_of_registration,
                end_of_registration=hackathon.end_of_registration,
                start_of_hack=hackathon.start_of_hack,
                end_of_hack=hackathon.end_of_hack,
                amount_money=hackathon.amount_money,
                type=hackathon.type,
            )
            for hackathon in hackathons
        ]
    )


@hackathon_router.post("/", response_model=HackathonCreatePostResponse, status_code=201)
async def upsert_hackathon(request: HackathonCreatePostRequest):
    """
    Создать или обновить новый хакатон.
    """
    logger.info(f"hackathon_post: {request.name}")
    hackathon_id = await hackathon_service.upsert_hackathon(
        name=request.name,
        task_description=request.task_description,
        start_of_registration=request.start_of_registration,
        end_of_registration=request.end_of_registration,
        start_of_hack=request.start_of_hack,
        end_of_hack=request.end_of_hack,
        amount_money=request.amount_money,
        type=request.type,
    )

    return HackathonCreatePostResponse(id=hackathon_id)


@hackathon_router.get("/{hackathon_id}", response_model=HackathonGetByIdResponse)
async def get_hackathon_by_id(hackathon_id: UUID):
    """
    Получить информацию о хакатоне по ID.
    """
    logger.info(f"hackathon_get_by_id: {hackathon_id}")
    hackathon, found = await hackathon_service.get_hackathon_by_id(hackathon_id)

    if not found:
        logger.error(f"hackathon_get_by_id: {hackathon_id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Хакатон не найден")

    return HackathonGetByIdResponse(
        id=hackathon.id,
        name=hackathon.name,
        task_description=hackathon.task_description,
        start_of_registration=hackathon.start_of_registration,
        end_of_registration=hackathon.end_of_registration,
        start_of_hack=hackathon.start_of_hack,
        end_of_hack=hackathon.end_of_hack,
        amount_money=hackathon.amount_money,
        type=hackathon.type,
    )

