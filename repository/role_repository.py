from loguru import logger

from infrastructure.db.connection import pg_connection
from persistent.db.role import Role
from sqlalchemy import insert, select


class RoleRepository:
    def __init__(self) -> None:
        self._sessionmaker = pg_connection()

    async def create_role(self, name: str) -> None:
        stmp = insert(Role).values({"name": name})

        async with self._sessionmaker() as session:
            await session.execute(stmp)
            await session.commit()

    async def get_role_by_id(self, role_id: int) -> dict | None:
        stmp = select(Role).where(Role.role_id == role_id).limit(1)

        async with self._sessionmaker() as session:
            resp = await session.execute(stmp)

        row = resp.fetchone()
        if row is None:
            return None

        return dict(row)

    async def get_role_by_name(self, name: str) -> Role | None:
        """
        Возвращает объект Role по его имени.
        """
        logger.debug(f"Поиск роли с именем: {name}")
        logger.debug(f"Тип Role.name: {type(Role.name)}")
        logger.debug(f"Тип name: {type(name)}")

        stmp = select(Role).where(Role.name == name).limit(1)

        async with self._sessionmaker() as session:
            resp = await session.execute(stmp)

            row = resp.fetchone()
            if row is None:
                logger.warning(f"Роль с именем {name} не найдена")
                return None

            role = row[0]  # Извлекаем объект Role из кортежа
            logger.debug(f"Найдена роль: {role}")
            return role
