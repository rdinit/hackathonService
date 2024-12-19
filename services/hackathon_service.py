from typing import List, Optional
from loguru import logger
from persistent.db.hackathon import Hackathon
from persistent.db.winner_solution import WinnerSolution
from repository.hackathon_repository import HackathonRepository


class HackathonService:
    def __init__(self) -> None:
        self.hackathon_repository = HackathonRepository()

    async def create_hackathon(
        self,
        name: str,
        task_description: str,
        start_of_registration: str,
        end_of_registration: str,
        start_of_hack: str,
        end_of_hack: str,
        amount_money: float,
        hack_type: str,
    ) -> Hackathon:
        """
        Создаёт новый хакатон.
        """
        return await self.hackathon_repository.create_hackathon(
            name, task_description, start_of_registration,
            end_of_registration, start_of_hack, end_of_hack,
            amount_money, hack_type
        )

    async def get_all_hackathons(self) -> List[Hackathon]:
        """
        Возвращает все хакатоны.
        """
        hackathons = await self.hackathon_repository.get_all_hackathons()
        if not hackathons:
            logger.warning("Хакатоны не найдены.")
        return hackathons

    async def get_hackathon_by_id(self, hackathon_id: str) -> Optional[Hackathon]:
        """
        Возвращает хакатон по его ID.
        """
        hackathon = await self.hackathon_repository.get_hackathon_by_id(hackathon_id)
        if not hackathon:
            logger.warning(f"Хакатон с ID {hackathon_id} не найден.")
        return hackathon

    async def add_winner_solution(
        self,
        hackathon_id: str,
        team_id: str,
        win_money: float,
        link_to_solution: str,
        link_to_presentation: str,
        can_share: bool = True,
    ) -> WinnerSolution:
        """
        Добавляет решение-победителя для хакатона.
        """
        return await self.hackathon_repository.add_winner_solution(
            hackathon_id, team_id, win_money, link_to_solution,
            link_to_presentation, can_share
        )

    async def add_hackathon_winner(self, hackathon_id: str, team_id: str) -> None:
        """
        Добавляет команду-победителя.
        """
        await self.hackathon_repository.add_hackathon_winner(hackathon_id, team_id)

    async def delete_hackathon(self, hackathon_id: str) -> None:
        """
        Удаляет хакатон.
        """
        await self.hackathon_repository.delete_hackathon(hackathon_id)
