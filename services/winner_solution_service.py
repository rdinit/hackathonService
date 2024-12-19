from typing import List, Optional
from loguru import logger
from persistent.db.winner_solution import WinnerSolution
from repository.winner_solution_repository import WinnerSolutionRepository


class WinnerSolutionService:
    def __init__(self) -> None:
        self.winner_solution_repository = WinnerSolutionRepository()

    async def create_winner_solution(
        self,
        hackathon_id: str,
        team_id: str,
        win_money: float,
        link_to_solution: str,
        link_to_presentation: str,
        can_share: bool = True,
    ) -> WinnerSolution:
        """
        Создаёт новое призерское решение.
        """
        return await self.winner_solution_repository.create_winner_solution(
            hackathon_id, team_id, win_money, link_to_solution,
            link_to_presentation, can_share
        )

    async def get_winner_solutions_by_hackathon(self, hackathon_id: str) -> List[WinnerSolution]:
        """
        Получение всех призерских решений для заданного хакатона.
        """
        solutions = await self.winner_solution_repository.get_winner_solutions_by_hackathon(hackathon_id)
        if not solutions:
            logger.warning(f"Призерские решения для хакатона {hackathon_id} не найдены.")
        return solutions

    async def get_winner_solution_by_id(self, solution_id: str) -> Optional[WinnerSolution]:
        """
        Получение призерского решения по ID.
        """
        solution = await self.winner_solution_repository.get_winner_solution_by_id(solution_id)
        if not solution:
            logger.warning(f"Призерское решение с ID {solution_id} не найдено.")
        return solution

    async def delete_winner_solution(self, solution_id: str) -> None:
        """
        Удаление призерского решения.
        """
        await self.winner_solution_repository.delete_winner_solution(solution_id)
