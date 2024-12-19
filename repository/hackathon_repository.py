from typing import List, Optional
from loguru import logger
from sqlalchemy import insert, select, delete
from sqlalchemy.orm import joinedload
from infrastructure.db.connection import pg_connection
from persistent.db.hackathon import Hackathon
from persistent.db.winner_solution import WinnerSolution
from persistent.db.relations import hackathon_winner_association


class HackathonRepository:
    def __init__(self) -> None:
        self._sessionmaker = pg_connection()

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
        Создание нового хакатона.
        """
        stmp = insert(Hackathon).values({
            "name": name,
            "task_description": task_description,
            "start_of_registration": start_of_registration,
            "end_of_registration": end_of_registration,
            "start_of_hack": start_of_hack,
            "end_of_hack": end_of_hack,
            "amount_money": amount_money,
            "type": hack_type,
        }).returning(Hackathon)

        async with self._sessionmaker() as session:
            resp = await session.execute(stmp)
            await session.commit()
            return resp.fetchone()[0]

    async def get_all_hackathons(self) -> List[Hackathon]:
        """
        Получение всех хакатонов.
        """
        stmp = select(Hackathon).options(joinedload(Hackathon.winner_solutions))

        async with self._sessionmaker() as session:
            resp = await session.execute(stmp)
            rows = resp.fetchall()
            return [row[0] for row in rows]

    async def get_hackathon_by_id(self, hackathon_id: str) -> Optional[Hackathon]:
        """
        Получение хакатона по ID.
        """
        stmp = select(Hackathon).where(Hackathon.id == hackathon_id).options(
            joinedload(Hackathon.winner_solutions)
        )

        async with self._sessionmaker() as session:
            resp = await session.execute(stmp)
            row = resp.fetchone()
            return row[0] if row else None

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
        Добавление решения-победителя для хакатона.
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

    async def add_hackathon_winner(self, hackathon_id: str, team_id: str) -> None:
        """
        Добавление команды-победителя в таблицу hackathon_winner.
        """
        stmp = insert(hackathon_winner_association).values({
            "hackathon_id": hackathon_id,
            "team_id": team_id,
        })

        async with self._sessionmaker() as session:
            await session.execute(stmp)
            await session.commit()

    async def delete_hackathon(self, hackathon_id: str) -> None:
        """
        Удаление хакатона по его ID.
        """
        stmp = delete(Hackathon).where(Hackathon.id == hackathon_id)

        async with self._sessionmaker() as session:
            await session.execute(stmp)
            await session.commit()
