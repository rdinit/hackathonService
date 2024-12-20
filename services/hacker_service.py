from uuid import UUID
from datetime import datetime
from typing import List, Optional
from loguru import logger

from infrastructure.db.connection import pg_connection
from persistent.db.hacker import Hacker
from persistent.db.role import Role
from repository.hacker_repository import HackerRepository


class HackerService:
    def __init__(self) -> None:
        self._sessionmaker = pg_connection()
        self.hacker_repository = HackerRepository()

    async def get_all_hackers(self) -> List[Hacker]:
        """
        Метод для получения всех хакеров.
        Использует метод репозитория для извлечения всех хакеров из базы данных.
        Возвращает список хакеров в виде словарей.
        """
        try:
            logger.info("Начинается получение всех хакеров из базы данных.")
            hackers = await self.hacker_repository.get_all_hackers()
            logger.info(f"Успешно получены {len(hackers)} хакеров.")
            return hackers
        except Exception as e:
            logger.exception("Ошибка при получении всех хакеров.")
            raise

    async def create_hacker(self, user_id: UUID, name: str) -> UUID:
        """
        Метод для создания нового хакера.
        """
        try:
            logger.info(f"Попытка создать хакера с user_id: {user_id} и именем: {name}.")
            existing_hacker = await self.hacker_repository.get_hacker_by_user_id(user_id)
            if existing_hacker:
                logger.warning(f"Хакер с user_id: {user_id} уже существует.")
                raise ValueError("Хакер с таким user_id уже существует.")

            hacker_id = await self.hacker_repository.add_hacker(user_id, name)
            logger.info(f"Хакер создан с ID: {hacker_id}.")
            return hacker_id
        except ValueError as ve:
            logger.error(str(ve))
            raise
        except Exception as e:
            logger.exception("Ошибка при создании хакера.")
            raise

    async def get_hacker_by_id(self, hacker_id: UUID) -> Optional[Hacker]:
        """
        Метод для поиска хакера по его уникальному ID.
        """
        try:
            logger.info(f"Поиск хакера с ID: {hacker_id}.")
            hacker = await self.hacker_repository.get_hacker_by_id(hacker_id)
            if hacker:
                logger.info(f"Хакер с ID: {hacker_id} найден.")
            else:
                logger.warning(f"Хакер с ID: {hacker_id} не найден.")
            return hacker
        except Exception as e:
            logger.exception(f"Ошибка при поиске хакера с ID: {hacker_id}.")
            raise

    async def get_hacker_by_user_id(self, user_id: UUID) -> Optional[Hacker]:
        """
        Метод для поиска хакера по его user_id (UUID).
        """
        try:
            logger.info(f"Поиск хакера с user_id: {user_id}.")
            hacker = await self.hacker_repository.get_hacker_by_user_id(user_id)
            if hacker:
                logger.info(f"Хакер с user_id: {user_id} найден.")
            else:
                logger.warning(f"Хакер с user_id: {user_id} не найден.")
            return hacker
        except Exception as e:
            logger.exception(f"Ошибка при поиске хакера с user_id: {user_id}.")
            raise

    async def add_roles_to_hacker(self, hacker_id: UUID, roles: List[Role]) -> None:
        """
        Метод для добавления ролей хакеру.
        """
        try:
            logger.info(f"Добавление ролей хакеру с ID: {hacker_id}.")
            hacker = await self.hacker_repository.get_hacker_by_id(hacker_id)
            if not hacker:
                logger.warning(f"Хакер с ID: {hacker_id} не найден.")
                raise ValueError("Хакер не найден.")

            existing_roles = {role.name for role in hacker.roles}
            new_roles = [role for role in roles if role.name not in existing_roles]
            hacker.roles.extend(new_roles)
            hacker.updated_at = datetime.utcnow()

            async with self._sessionmaker() as session:
                session.add(hacker)
                await session.commit()
            logger.info(f"Роли успешно добавлены хакеру с ID: {hacker_id}.")
        except ValueError as ve:
            logger.error(str(ve))
            raise
        except Exception as e:
            logger.exception(f"Ошибка при добавлении ролей хакеру с ID: {hacker_id}.")
            raise

    async def update_hacker_roles(self, hacker_id: UUID, roles: List[Role]) -> None:
        """
        Метод для обновления ролей хакера.
        """
        try:
            logger.info(f"Обновление ролей хакеру с ID: {hacker_id}.")
            hacker = await self.hacker_repository.get_hacker_by_id(hacker_id)
            if not hacker:
                logger.warning(f"Хакер с ID: {hacker_id} не найден.")
                raise ValueError("Хакер не найден.")

            hacker.roles = roles
            hacker.updated_at = datetime.utcnow()

            async with self._sessionmaker() as session:
                session.add(hacker)
                await session.commit()
            logger.info(f"Роли успешно обновлены для хакера с ID: {hacker_id}.")
        except ValueError as ve:
            logger.error(str(ve))
            raise
        except Exception as e:
            logger.exception(f"Ошибка при обновлении ролей хакера с ID: {hacker_id}.")
            raise
