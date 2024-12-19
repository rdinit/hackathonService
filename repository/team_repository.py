from typing import cast, List, Optional

from loguru import logger

from infrastructure.db.connection import pg_connection
from persistent.db.team import Team
from sqlalchemy import insert, select, delete


class TeamRepository:
    def __init__(self) -> None:
        self._sessionmaker = pg_connection()

    async def create_team(self, owner_uuid: str, name: str, size: int) -> Team:
        """
        Создание новой команды в базе данных.
        """
        stmp = insert(Team).values({
            "owner_uuid": owner_uuid,
            "name": name,
            "size": size,
        }).returning(Team)

        async with self._sessionmaker() as session:
            resp = await session.execute(stmp)
            await session.commit()

            row = resp.fetchone()
            return row[0] if row else None

    async def get_all_teams(self) -> List[Team]:
        """
        Получение всех команд из базы данных.
        """
        stmp = select(Team)

        async with self._sessionmaker() as session:
            resp = await session.execute(stmp)
            rows = resp.fetchall()

            teams = [row[0] for row in rows]  # Преобразуем строки в объекты Team
            return teams

    async def get_team_by_id(self, team_id: str) -> Optional[Team]:
        """
        Получение команды по её идентификатору.
        """
        stmp = select(Team).where(cast("ColumnElement[bool]", Team.id == team_id)).limit(1)

        async with self._sessionmaker() as session:
            resp = await session.execute(stmp)
            row = resp.fetchone()

            return row[0] if row else None

    async def get_team_by_name(self, name: str) -> Optional[Team]:
        """
        Получение команды по её имени.
        """
        stmp = select(Team).where(cast("ColumnElement[bool]", Team.name == name)).limit(1)

        async with self._sessionmaker() as session:
            resp = await session.execute(stmp)
            row = resp.fetchone()

            return row[0] if row else None

    async def add_hacker_to_team(self, team_id: str, hacker_id: str) -> None:
        """
        Добавление участника в команду (запись в таблицу связи).
        """
        from persistent.db.relations import hacker_team_association

        stmp = insert(hacker_team_association).values({
            "hacker_id": hacker_id,
            "team_id": team_id,
        })

        async with self._sessionmaker() as session:
            await session.execute(stmp)
            await session.commit()

    async def remove_hacker_from_team(self, team_id: str, hacker_id: str) -> None:
        """
        Удаление участника из команды (удаление из таблицы связи).
        """
        from persistent.db.relations import hacker_team_association

        stmp = delete(hacker_team_association).where(
            cast("ColumnElement[bool]", hacker_team_association.c.team_id == team_id),
            cast("ColumnElement[bool]", hacker_team_association.c.hacker_id == hacker_id),
        )

        async with self._sessionmaker() as session:
            await session.execute(stmp)
            await session.commit()

    async def delete_team(self, team_id: str) -> None:
        """
        Удаление команды по её идентификатору.
        """
        stmp = delete(Team).where(cast("ColumnElement[bool]", Team.id == team_id))

        async with self._sessionmaker() as session:
            await session.execute(stmp)
            await session.commit()
