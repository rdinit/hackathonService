from datetime import datetime
from typing import cast, List, Optional

from loguru import logger
from sqlalchemy.exc import IntegrityError

from infrastructure.db.connection import pg_connection
from persistent.db.hacker import Hacker
from sqlalchemy import select, update, delete, UUID, String
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker


class HackerRepository:
    def __init__(self) -> None:
        self._sessionmaker = pg_connection()

    async def get_all_hackers(self) -> List[Hacker]:
        """
        Метод для получения всех хакеров.
        Возвращает список хакеров из базы данных.
        """
        stmt = select(Hacker)

        async with self._sessionmaker() as session:
            resp = await session.execute(stmt)

            rows = resp.fetchall()  # Извлекаем все строки
            hackers = [row[0] for row in rows]  # Преобразуем их в список объектов Hacker
            return hackers

    async def upsert_hacker(self, user_id: UUID, name: str) -> Optional[UUID]:

        # Создание хакера без ролей
        stmt = insert(Hacker).values({
            "user_id": user_id,
            "name": name
        })

        stmt.on_conflict_do_update(constraint="uq_hacker_user_id", set_={
            "name": name,
            "updated_at": datetime.utcnow(),
        })

        async with self._sessionmaker() as session:
            # Добавление хакера
            result = await session.execute(stmt)
            hacker_id = result.inserted_primary_key[0]

            await session.commit()

        return hacker_id

    async def update_hacker_roles(self, hacker_id: UUID, roles: List[String]) -> bool:

        hacker = await self.get_hacker_by_id(hacker_id)

        if not hacker:
            raise ValueError("Хакер не найден")

        hacker.roles = roles

        async with self._sessionmaker() as session:
            try:
                await session.commit()
            except IntegrityError as error:
                await session.rollback()
                return False

        return True

    async def get_hacker_by_id(self, hacker_id: UUID) -> Optional[Hacker]:
        # Используем user_uuid для поиска хакера
        stmt = select(Hacker).where(cast("ColumnElement[bool]", Hacker.id == hacker_id)).limit(1)

        async with self._sessionmaker() as session:
            resp = await session.execute(stmt)

        row = resp.fetchone()
        return row[0] if row else None

    async def get_hacker_by_user_id(self, user_id: UUID) -> Optional[Hacker]:
        # Используем user_uuid для поиска хакера
        stmt = select(Hacker).where(cast("ColumnElement[bool]", Hacker.user_id == user_id)).limit(1)

        async with self._sessionmaker() as session:
            resp = await session.execute(stmt)

        row = resp.fetchone()
        return row[0] if row else None
