from datetime import datetime
from typing import List, Optional, Tuple
from loguru import logger
from sqlalchemy import UUID

from infrastructure.db.connection import pg_connection
from persistent.db.winner_solution import WinnerSolution
from repository.hackathon_repository import HackathonRepository
from repository.team_repository import TeamRepository
from repository.winner_solution_repository import WinnerSolutionRepository


class WinnerSolutionService:
    def __init__(self) -> None:
        self.winner_solution_repository = WinnerSolutionRepository()

    async def get_all_winner_solutions(self) -> List[WinnerSolution]:
        """
        Возвращает все хакатоны.
        """
        winner_solutions = await self.winner_solution_repository.get_all_winner_solutions()

        return winner_solutions

    async def create_winner_solution(
        self,
        hackathon_id: UUID,
        team_id: UUID,
        win_money: float,
        link_to_solution: str,
        link_to_presentation: str,
        can_share: bool = True,
    ) -> Tuple[UUID, bool]:
        """
        Создаёт новое призерское решение.

        :returns False Решение от этой команды уже записано
        """
        winner_solutions_id = await self.winner_solution_repository.create_winner_solution(
            hackathon_id, team_id, win_money, link_to_solution, link_to_presentation, can_share
        )

        if not winner_solutions_id:
            return None, False

        return winner_solutions_id, True

    async def get_winner_solution_by_id(self, solution_id: UUID) -> Tuple[WinnerSolution, bool]:
        """
        Получение призерского решения по ID.

        :returns False Решение не найдено
        """
        winner_solution = await self.winner_solution_repository.get_winner_solution_by_id(solution_id)

        if not winner_solution:
            return None, False

        return winner_solution, True
