from datetime import datetime
from typing import cast, List

from loguru import logger

from infrastructure.db.connection import pg_connection
from persistent.db.hacker import Hacker
from persistent.db.role import Role
from sqlalchemy import insert, select, update, delete, UUID
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
        stmp = select(Hacker)

        async with self._sessionmaker() as session:
            resp = await session.execute(stmp)

            rows = resp.fetchall()  # Извлекаем все строки
            hackers = [row[0] for row in rows]  # Преобразуем их в список объектов Hacker
            return hackers

    async def add_hacker(self, user_id: UUID, name: str) -> UUID | None:
        created_at = updated_at = datetime.utcnow()  # Текущее время для created_at и updated_at

        # Создание хакера без ролей
        stmt = insert(Hacker).values({
            "user_id": user_id,
            "name": name,
            "created_at": created_at,
            "updated_at": updated_at
        })

        async with self._sessionmaker() as session:
            # Добавление хакера
            result = await session.execute(stmt)
            hacker_id = result.inserted_primary_key[0]
            await session.commit()

        return hacker_id

    async def update_roles(self, hacker_id: UUID, roles: List[Role] = None) -> None:
        """
        Метод для обновления данных хакера по его ID.
        Обновляются только те поля, которые переданы в аргументах (name и/или roles).
        """
        updated_at = datetime.utcnow()

        # Формируем словарь с обновляемыми данными
        update_data = {"updated_at": updated_at}

        if roles is not None:
            update_data["roles"] = roles  # Если роли передаются, обновляем их

        stmt = update(Hacker).where(cast("ColumnElement[bool]", Hacker.id == hacker_id)).values(update_data)

        async with self._sessionmaker() as session:
            # Выполняем запрос на обновление
            result = await session.execute(stmt)
            await session.commit()

    async def get_hacker_by_id(self, hacker_id: UUID) -> Hacker | None:
        # Используем user_uuid для поиска хакера
        stmt = select(Hacker).where(cast("ColumnElement[bool]", Hacker.id == hacker_id)).limit(1)

        async with self._sessionmaker() as session:
            resp = await session.execute(stmt)

        row = resp.fetchone()
        return row[0]

    async def get_hacker_by_user_id(self, user_id: UUID) -> Hacker | None:
        # Используем user_uuid для поиска хакера
        stmt = select(Hacker).where(cast("ColumnElement[bool]", Hacker.user_uuid == user_id)).limit(1)

        async with self._sessionmaker() as session:
            resp = await session.execute(stmt)

        row = resp.fetchone()
        return row
