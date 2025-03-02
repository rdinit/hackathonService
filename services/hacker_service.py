from uuid import UUID
from datetime import datetime
from typing import List, Optional
from loguru import logger

from infrastructure.db.connection import pg_connection
from persistent.db.hacker import Hacker
from persistent.db.role import Role
from repository.hacker_repository import HackerRepository
from repository.role_repository import RoleRepository


class HackerService:
    def __init__(self) -> None:
        self._sessionmaker = pg_connection()
        self.hacker_repository = HackerRepository()
        self.role_repository = RoleRepository()

    async def get_all_hackers(self) -> List[Hacker]:
        """
        Метод для получения всех хакатонщиков.
        Использует метод репозитория для извлечения всех хакеров из базы данных.
        Возвращает список хакатонщиков в виде словарей.
        """
        hackers = await self.hacker_repository.get_all_hackers()
        if not hackers:
            logger.warning("Хакатонщики не найдены.")
        return hackers

    async def create_hacker(self, user_id: UUID, name: str) -> UUID:
        """
        Метод для создания нового хакатонщика.
        """

        existing_hacker = await self.hacker_repository.get_hacker_by_user_id(user_id)
        if existing_hacker:
            raise ValueError("Хакатонщик с таким user_id уже существует.")

        hacker_id = await self.hacker_repository.add_hacker(user_id, name)

        return hacker_id

        try:
            existing_hacker = await self.hacker_repository.get_hacker_by_user_id(user_id)
            if existing_hacker:
                raise ValueError("Хакатонщик с таким user_id уже существует.")

            hacker_id = await self.hacker_repository.add_hacker(user_id, name)
            return hacker_id
        except ValueError as ve:
            logger.error(str(ve))
            raise
        except Exception as e:
            logger.exception("Ошибка при создании Хакатонщика.")
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
            logger.exception(f"Ошибка при поиске Хакатонщика с ID: {hacker_id}.")
            raise

    async def get_hacker_by_user_id(self, user_id: UUID) -> Optional[Hacker]:
        """
        Метод для поиска хакера по его user_id (UUID).
        """
        try:
            logger.info(f"Поиск Хакатонщика с user_id: {user_id}.")
            hacker = await self.hacker_repository.get_hacker_by_user_id(user_id)
            if hacker:
                logger.info(f"Хакатонщик с user_id: {user_id} найден.")
            else:
                logger.warning(f"Хакатонщик с user_id: {user_id} не найден.")
            return hacker
        except Exception as e:
            logger.exception(f"Ошибка при поиске Хакатонщика с user_id: {user_id}.")
            raise

    async def add_roles_to_hacker(self, hacker_id: UUID, roles: List[UUID]) -> None:
        """
        Метод для добавления ролей хакеру.
        """
        try:
            logger.info(f"Добавление ролей хакеру с ID: {hacker_id}.")
            hacker = await self.hacker_repository.get_hacker_by_id(hacker_id)
            if not hacker:
                logger.warning(f"Хакатонщик с ID: {hacker_id} не найден.")
                raise ValueError("Хакатонщик не найден.")

            existing_roles = [role.id for role in hacker.roles]
            new_roles = [await self.role_repository.get_role_by_id(role_id) for role_id in roles if role_id not in existing_roles]
            hacker.roles.extend(new_roles)
            hacker.updated_at = datetime.utcnow()

            async with self._sessionmaker() as session:
                session.add(hacker)
                await session.commit()
            logger.info(f"Роли успешно добавлены Хакатонщику с ID: {hacker_id}.")
        except ValueError as ve:
            logger.error(str(ve))
            raise
        except Exception as e:
            logger.exception(f"Ошибка при добавлении ролей Хакатонщику с ID: {hacker_id}.")
            raise

    async def update_hacker_roles(self, hacker_id: UUID, roles: List[Role]) -> None:
        """
        Метод для обновления ролей хакера.
        """
        try:
            logger.info(f"Обновление ролей хакеру с ID: {hacker_id}.")
            hacker = await self.hacker_repository.get_hacker_by_id(hacker_id)
            if not hacker:
                logger.warning(f"Хакатонщик с ID: {hacker_id} не найден.")
                raise ValueError("Хакатонщик не найден.")

            hacker.roles = roles
            hacker.updated_at = datetime.utcnow()

            async with self._sessionmaker() as session:
                session.add(hacker)
                await session.commit()
            logger.info(f"Роли успешно обновлены для Хакатонщика с ID: {hacker_id}.")
        except ValueError as ve:
            logger.error(str(ve))
            raise
        except Exception as e:
            logger.exception(f"Ошибка при обновлении ролей Хакатонщика с ID: {hacker_id}.")
            raise
