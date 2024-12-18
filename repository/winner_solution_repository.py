from typing import List, Optional
from loguru import logger
from sqlalchemy import insert, select, delete
from infrastructure.db.connection import pg_connection
from persistent.db.winner_solution import WinnerSolution


class WinnerSolutionRepository:
    def __init__(self) -> None:
        self._sessionmaker = pg_connection()

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
        Создание нового призерского решения.
        """
        stmp = insert(WinnerSolution).values({
            "hack_uuid": hackathon_id,
            "team_uuid": team_id,
            "win_money": win_money,
            "link_to_solution": link_to_solution,
            "link_to_presentation": link_to_presentation,
            "can_share": can_share,
        }).returning(WinnerSolution)

        async with self._sessionmaker() as session:
            resp = await session.execute(stmp)
            await session.commit()
            return resp.fetchone()[0]

    async def get_winner_solutions_by_hackathon(self, hackathon_id: str) -> List[WinnerSolution]:
        """
        Получение всех призерских решений для конкретного хакатона.
        """
        stmp = select(WinnerSolution).where(WinnerSolution.hack_uuid == hackathon_id)

        async with self._sessionmaker() as session:
            resp = await session.execute(stmp)
            rows = resp.fetchall()
            return [row[0] for row in rows]

    async def get_winner_solution_by_id(self, solution_id: str) -> Optional[WinnerSolution]:
        """
        Получение призерского решения по ID.
        """
        stmp = select(WinnerSolution).where(WinnerSolution.id == solution_id)

        async with self._sessionmaker() as session:
            resp = await session.execute(stmp)
            row = resp.fetchone()
            return row[0] if row else None

    async def delete_winner_solution(self, solution_id: str) -> None:
        """
        Удаление призерского решения по его ID.
        """
        stmp = delete(WinnerSolution).where(WinnerSolution.id == solution_id)

        async with self._sessionmaker() as session:
            await session.execute(stmp)
            await session.commit()
