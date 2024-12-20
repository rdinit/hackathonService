from typing import cast, List

from loguru import logger

from infrastructure.db.connection import pg_connection
from persistent.db.role import Role
from sqlalchemy import insert, select, UUID


class RoleRepository:
    def __init__(self) -> None:
        self._sessionmaker = pg_connection()

    async def create_role(self, name: str) -> None:
        stmt = insert(Role).values({"name": name})

        async with self._sessionmaker() as session:
            await session.execute(stmt)
            await session.commit()

    async def get_all_roles(self) -> List[Role]:
        """
        Метод для получения всех ролей из базы данных.
        """
        stmt = select(Role)

        async with self._sessionmaker() as session:
            resp = await session.execute(stmt)

            rows = resp.fetchall()  # Извлекаем все строки
            roles = [row[0] for row in rows]  # Преобразуем их в список объектов Role
            return roles

    async def get_role_by_id(self, role_id: UUID) -> Role | None:
        stmt = select(Role).where(cast("ColumnElement[bool]", Role.id == role_id)).limit(1)

        async with self._sessionmaker() as session:
            resp = await session.execute(stmt)

        row = resp.fetchone()
        return row[0]

    async def get_role_by_name(self, name: str) -> Role | None:
        """
        Возвращает объект Role по его имени.
        """
        logger.debug(f"Поиск роли с именем: {name}")
        logger.debug(f"Тип Role.name: {type(Role.name)}")
        logger.debug(f"Тип name: {type(name)}")

        stmt = select(Role).where(cast("ColumnElement[bool]", Role.name == name)).limit(1)

        async with self._sessionmaker() as session:
            resp = await session.execute(stmt)

            row = resp.fetchone()
            return row[0] if row else None
