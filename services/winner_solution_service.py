from datetime import datetime
from typing import List, Optional
from loguru import logger
from sqlalchemy import UUID

from infrastructure.db.connection import pg_connection
from persistent.db.winner_solution import WinnerSolution
from repository.hackathon_repository import HackathonRepository
from repository.team_repository import TeamRepository
from repository.winner_solution_repository import WinnerSolutionRepository


class WinnerSolutionService:
    def __init__(self) -> None:
        self._sessionmaker = pg_connection()
        self.winner_solution_repository = WinnerSolutionRepository()
        self.hackathon_repository = HackathonRepository()
        self.team_repository = TeamRepository()

    async def get_all_hackathons(self) -> List[WinnerSolution]:
        """
        Возвращает все хакатоны.
        """
        winner_solutions = await self.winner_solution_repository.get_all_winner_solutions()
        if not winner_solutions:
            logger.warning("Решения не найдены.")
        return winner_solutions

    async def create_winner_solution(
        self,
        hackathon_id: UUID,
        team_id: UUID,
        win_money: float,
        link_to_solution: str,
        link_to_presentation: str,
        can_share: bool = True,
    ) -> UUID:
        """
        Создаёт новое призерское решение.
        """
        winner_solutions_id = await self.winner_solution_repository.create_winner_solution(
            win_money, link_to_solution, link_to_presentation, can_share
        )
        winner_solution = await self.winner_solution_repository.get_winner_solution_by_id(winner_solutions_id)
        hackathon = await self.hackathon_repository.get_hackathon_by_id(hackathon_id)
        team = await self.team_repository.get_team_by_id(team_id)

        # TODO: проверить наличие хакатона и команды (возможно запрашивать через их сервис)

        winner_solution.hackathon = hackathon
        winner_solution.team = team

        # Сохраняем изменения в базе данных
        async with self._sessionmaker() as session:
            # Для того чтобы изменения были зафиксированы в базе данных
            session.add(winner_solution)
            await session.commit()  # Совершаем коммит

        logger.info(f"Решение для хакатона '{hackathon_id}' успешно создано.")

        return winner_solutions_id

    async def get_winner_solution_by_id(self, solution_id: UUID) -> Optional[WinnerSolution]:
        """
        Получение призерского решения по ID.
        """
        winner_solution = await self.winner_solution_repository.get_winner_solution_by_id(solution_id)
        if not winner_solution:
            logger.warning(f"Призерское решение с ID {solution_id} не найдено.")
        return winner_solution
