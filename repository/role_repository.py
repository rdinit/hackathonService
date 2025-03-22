from typing import List, Optional
from uuid import UUID

from sqlalchemy import cast, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from infrastructure.db.connection import pg_connection
from persistent.db.role import Role


class RoleRepository:
    def __init__(self) -> None:
        self._sessionmaker = pg_connection()

    async def upsert_role(self, name: str) -> Optional[UUID]:
        """
        Создание или обновление роли в базе данных.
        """
        stmt = insert(Role).values({
            "name": name,
        })
        
        async with self._sessionmaker() as session:
            result = await session.execute(stmt)
            role_id = result.inserted_primary_key[0]

            try:
                await session.commit()
            except IntegrityError as error:
                await session.rollback()
                return None

        return role_id

    async def get_all_roles(self) -> List[Role]:
        """
        Получение всех ролей из базы данных.
        """
        stmt = select(Role)

        async with self._sessionmaker() as session:
            resp = await session.execute(stmt)

        return [row[0] for row in resp.fetchall()]

    async def get_role_by_id(self, role_id: UUID) -> Optional[Role]:
        """
        Получение роли по её идентификатору.
        """
        stmt = select(Role).where(cast("ColumnElement[bool]", Role.id == role_id)).limit(1)

        async with self._sessionmaker() as session:
            resp = await session.execute(stmt)

        row = resp.fetchone()
        return row[0] if row else None