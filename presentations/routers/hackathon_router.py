from datetime import datetime
from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from loguru import logger

from services.hackathon_service import HackathonService

hackathon_service = HackathonService()  # Создаём экземпляр HackathonService

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
    type: str  # "online" или "offline"


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
    type: str  # "online" или "offline"


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
    type: str  # "online" или "offline"


@hackathon_router.get("/", response_model=HackathonGetAllResponse)
async def get_all_hackathons():
    """
    Получить список всех хакатонов.
    """
    logger.info("Начало обработки запроса на получение всех хакатонов.")
    try:
        hackathons = await hackathon_service.get_all_hackathons()
        logger.info(f"Успешно получено {len(hackathons)} хакатонов.")
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
    except Exception as e:
        logger.exception("Ошибка при получении списка хакатонов.")
        raise HTTPException(status_code=400, detail=str(e))


@hackathon_router.post("/", response_model=HackathonCreatePostResponse, status_code=201)
async def create_hackathon(hackathon_request: HackathonCreatePostRequest):
    """
    Создать новый хакатон.
    """
    logger.info(f"Попытка создания нового хакатона: {hackathon_request.name}.")
    try:
        hackathon_id = await hackathon_service.create_hackathon(
            name=hackathon_request.name,
            task_description=hackathon_request.task_description,
            start_of_registration=hackathon_request.start_of_registration,
            end_of_registration=hackathon_request.end_of_registration,
            start_of_hack=hackathon_request.start_of_hack,
            end_of_hack=hackathon_request.end_of_hack,
            amount_money=hackathon_request.amount_money,
            type=hackathon_request.type,
        )
        logger.info(f"Хакатон успешно создан с ID: {hackathon_id}.")
        return HackathonCreatePostResponse(id=hackathon_id)
    except Exception as e:
        logger.exception("Ошибка при создании хакатона.")
        raise HTTPException(status_code=400, detail=str(e))


@hackathon_router.get("/{hackathon_id}", response_model=HackathonGetByIdResponse)
async def get_hackathon_by_id(hackathon_id: UUID):
    """
    Получить информацию о хакатоне по ID.
    """
    logger.info(f"Начало поиска хакатона с ID: {hackathon_id}.")
    try:
        hackathon = await hackathon_service.get_hackathon_by_id(hackathon_id)
        if not hackathon:
            logger.warning(f"Хакатон с ID: {hackathon_id} не найден.")
            raise HTTPException(status_code=404, detail="Хакатон не найден")

        logger.info(f"Хакатон с ID: {hackathon_id} найден.")
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
    except HTTPException:
        logger.warning(f"Хакатон с ID: {hackathon_id} не найден.")
        raise
    except Exception as e:
        logger.exception(f"Ошибка при поиске хакатона с ID: {hackathon_id}.")
        raise HTTPException(status_code=400, detail=str(e))
