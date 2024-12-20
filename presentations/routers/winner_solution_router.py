from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from loguru import logger

from services.winner_solution_service import WinnerSolutionService

winner_solution_service = WinnerSolutionService()

winner_solution_router = APIRouter(
    prefix="/winner-solution",
    tags=["Winner Solutions"],
    responses={404: {"description": "Not Found"}},
)


class WinnerSolutionDto(BaseModel):
    id: UUID
    win_money: float
    link_to_solution: str
    link_to_presentation: str
    can_share: bool
    hackathon_id: UUID
    team_id: UUID


class WinnerSolutionGetAllResponse(BaseModel):
    winner_solutions: List[WinnerSolutionDto]


class WinnerSolutionCreatePostRequest(BaseModel):
    win_money: float
    link_to_solution: str
    link_to_presentation: str
    can_share: bool
    hackathon_id: UUID
    team_id: UUID


class WinnerSolutionCreatePostResponse(BaseModel):
    id: UUID


class WinnerSolutionGetByIdResponse(BaseModel):
    id: UUID
    win_money: float
    link_to_solution: str
    link_to_presentation: str
    can_share: bool
    hackathon_id: UUID
    team_id: UUID


@winner_solution_router.get("/", response_model=WinnerSolutionGetAllResponse)
async def get_all_winner_solutions():
    """
    Получить список всех призерских решений.
    """
    logger.info("Запрос на получение списка всех призерских решений.")
    try:
        winner_solutions = await winner_solution_service.get_all_winner_solutions()
        logger.info(f"Получено {len(winner_solutions)} призерских решений.")
        return WinnerSolutionGetAllResponse(
            winner_solutions=[
                WinnerSolutionDto(
                    id=solution.id,
                    win_money=solution.win_money,
                    link_to_solution=solution.link_to_solution,
                    link_to_presentation=solution.link_to_presentation,
                    can_share=solution.can_share,
                    hackathon_id=solution.hackathon_id,
                    team_id=solution.team_id,
                )
                for solution in winner_solutions
            ]
        )
    except Exception as e:
        logger.exception("Ошибка при получении списка призерских решений.")
        raise HTTPException(status_code=400, detail="Не удалось получить список призерских решений.")


@winner_solution_router.post("/", response_model=WinnerSolutionCreatePostResponse, status_code=201)
async def create_winner_solution(solution_request: WinnerSolutionCreatePostRequest):
    """
    Создать новое призерское решение.
    """
    logger.info(f"Попытка создания призерского решения для команды {solution_request.team_id} и хакатона {solution_request.hackathon_id}.")
    try:
        solution_id = await winner_solution_service.create_winner_solution(
            win_money=solution_request.win_money,
            link_to_solution=solution_request.link_to_solution,
            link_to_presentation=solution_request.link_to_presentation,
            can_share=solution_request.can_share,
            hackathon_id=solution_request.hackathon_id,
            team_id=solution_request.team_id,
        )
        logger.info(f"Призерское решение успешно создано с ID: {solution_id}.")
        return WinnerSolutionCreatePostResponse(id=solution_id)
    except Exception as e:
        logger.exception("Ошибка при создании призерского решения.")
        raise HTTPException(status_code=400, detail="Не удалось создать призерское решение.")


@winner_solution_router.get("/{solution_id}", response_model=WinnerSolutionGetByIdResponse)
async def get_winner_solution_by_id(solution_id: UUID):
    """
    Получить информацию о призерском решении по ID.
    """
    logger.info(f"Запрос на получение информации о призерском решении с ID {solution_id}.")
    try:
        solution = await winner_solution_service.get_winner_solution_by_id(solution_id)
        if not solution:
            logger.warning(f"Призерское решение с ID {solution_id} не найдено.")
            raise HTTPException(status_code=404, detail="Решение не найдено")

        logger.info(f"Призерское решение с ID {solution_id} найдено.")
        return WinnerSolutionGetByIdResponse(
            id=solution.id,
            win_money=solution.win_money,
            link_to_solution=solution.link_to_solution,
            link_to_presentation=solution.link_to_presentation,
            can_share=solution.can_share,
            hackathon_id=solution.hackathon_id,
            team_id=solution.team_id,
        )
    except Exception as e:
        logger.exception(f"Ошибка при получении информации о призерском решении с ID {solution_id}.")
        raise HTTPException(status_code=400, detail="Не удалось получить информацию о призерском решении.")
