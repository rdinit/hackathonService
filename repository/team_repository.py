from typing import Tuple, cast, List, Optional

from loguru import logger
from sqlalchemy.exc import IntegrityError

from infrastructure.db.connection import pg_connection
from persistent.db.hacker import Hacker
from persistent.db.team import Team
from sqlalchemy import ColumnElement, select, delete, UUID
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import selectinload


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

    async def get_teams_by_user_id(self, user_id: UUID) -> List[Team]:
        """
        Получение всех команд, в которых пользователь с указанным user_id является участником.
        
        Ищет хакера по user_id и возвращает все команды, в которых он состоит.
        """
        async with self._sessionmaker() as session:
            # Сначала находим хакера по user_id
            hacker_stmt = select(Hacker).where(cast("ColumnElement[bool]", Hacker.user_id == user_id))
            hacker_result = await session.execute(hacker_stmt)
            hacker_rows = hacker_result.fetchall()
            
            if not hacker_rows:
                logger.warning(f"Хакер с user_id={user_id} не найден")
                return []
                
            hacker = hacker_rows[0][0]
            
            # Получаем ID команд, в которых состоит хакер
            team_ids = [team.id for team in hacker.teams]
            
            if not team_ids:
                logger.info(f"Хакер с user_id={user_id} не состоит ни в одной команде")
                return []
                
            # Загружаем полную информацию о командах, включая связанных хакеров
            teams_stmt = select(Team).where(Team.id.in_(team_ids)).options(selectinload(Team.hackers))
            teams_result = await session.execute(teams_stmt)
            teams = [row[0] for row in teams_result.fetchall()]
            
            return teams
