from typing import Tuple, cast, List, Optional

from loguru import logger
from sqlalchemy.exc import IntegrityError

from infrastructure.db.connection import pg_connection
from persistent.db.hacker import Hacker
from persistent.db.team import Team
from sqlalchemy import ColumnElement, select, delete, UUID
from sqlalchemy.dialects.postgresql import insert


class TeamRepository:
    def __init__(self) -> None:
        self._sessionmaker = pg_connection()

    async def get_all_teams(self) -> List[Team]:
        """
        Получение всех команд из базы данных.
        """
        stmt = select(Team)

        async with self._sessionmaker() as session:
            resp = await session.execute(stmt)

            rows = resp.fetchall()  # Извлекаем все строки
            teams = [row[0] for row in rows]  # Преобразуем их в список объектов Hacker
            return teams

    async def create_team(self, owner_id: UUID, name: str, max_size: int) -> Optional[UUID]:
        """
        Создание новой команды в базе данных.
        """
        stmt = insert(Team).values({
            "owner_id": owner_id,
            "name": name,
            "max_size": max_size,
        })

        async with self._sessionmaker() as session:
            result = await session.execute(stmt)
            team_id = result.inserted_primary_key[0]

            try:
                await session.commit()
            except IntegrityError as error:
                await session.rollback()
                return None

        return team_id

    async def add_hacker_to_team(self, team_id: UUID, hacker: Hacker) -> Tuple[Optional[Team], int]:
        """
        Добавление участника в команду.

        :returns -1 Команда не найдена
        :returns -2 Команда уже заполнена
        """
        async with self._sessionmaker() as session:
            stmt = select(Team).where(cast("ColumnElement[bool]", Team.id == team_id)).limit(1)
            resp = await session.execute(stmt)
            row = resp.fetchone()
            
            if not row:
                return None, -1
                
            team = row[0]
            
            if len(team.hackers) >= team.max_size:
                return None, -2
                
            team.hackers.append(hacker)
            await session.commit()
            
            return team, 1

    async def get_team_by_id(self, team_id: UUID) -> Optional[Team]:
        """
        Получение команды по её идентификатору.
        """
        stmt = select(Team).where(cast("ColumnElement[bool]", Team.id == team_id)).limit(1)

        async with self._sessionmaker() as session:
            resp = await session.execute(stmt)

        row = resp.fetchone()
        return row[0] if row else None

    async def get_team_by_name(self, name: str) -> Optional[Team]:
        """
        Получение команды по её имени.
        """
        stmt = select(Team).where(cast("ColumnElement[bool]", Team.name == name)).limit(1)

        async with self._sessionmaker() as session:
            resp = await session.execute(stmt)

        row = resp.fetchone()
        return row[0] if row else None
