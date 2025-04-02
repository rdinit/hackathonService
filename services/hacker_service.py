from uuid import UUID
from datetime import datetime
from typing import List, Optional, Tuple
from loguru import logger
from sqlalchemy import String

from infrastructure.db.connection import pg_connection
from persistent.db.hacker import Hacker
from persistent.db.role import RoleEnum
from repository.hacker_repository import HackerRepository


class HackerService:
    def __init__(self) -> None:
        self.hacker_repository = HackerRepository()

    async def get_all_hackers(self) -> List[Hacker]:
        """
        Возвращает всех хакатонщиков.
        """
        hackers = await self.hacker_repository.get_all_hackers()

        return hackers

    async def upsert_hacker(self, user_id: UUID, name: str) -> Tuple[Optional[UUID], bool]:
        """
        Создаёт или обновляет хакатонщика.
        
        Returns:
            Tuple[Optional[UUID], bool]: (id хакатонщика, успешно ли выполнена операция)
        """
        hacker_id = await self.hacker_repository.upsert_hacker(user_id, name)
        
        if hacker_id is None:
            logger.error(f"Не удалось создать или обновить хакатонщика с user_id={user_id}")
            return None, False
            
        return hacker_id, True

    async def get_hacker_by_id(self, hacker_id: UUID) -> Tuple[Hacker, bool]:
        """
        Возвращает хакера по ID.

        :returns False Хакер не найден
        """
        hacker = await self.hacker_repository.get_hacker_by_id(hacker_id)

        if not hacker:
            return None, False

        return hacker, True

    async def get_hacker_by_user_id(self, user_id: UUID) -> Tuple[Hacker, bool]:
        """
        Возвращает хакера по user_id (UUID).

        :returns False Хакер не найден
        """
        hacker = await self.hacker_repository.get_hacker_by_user_id(user_id)

        if not hacker:
            return None, False

        return hacker, True

    async def update_hacker_roles(self, hacker_id: UUID, role_ids: List[UUID]) -> bool:
        """
        Метод для обновления ролей хакера.

        :returns: False если произошла ошибка (хакер не найден или недопустимые роли)
        """
        return await self.hacker_repository.update_hacker_roles(hacker_id, role_ids)
        
    async def update_hacker_roles_by_user_id(self, user_id: UUID, role_names: List[str]) -> bool:
        """
        Метод для обновления ролей хакера по user_id и именам ролей.
        
        :returns: False если произошла ошибка (хакер не найден или недопустимые роли)
        """
        # Сначала получаем хакера по user_id
        hacker, found = await self.get_hacker_by_user_id(user_id)
        
        if not found:
            logger.error(f"Не удалось найти хакера с user_id={user_id}")
            return False
            
        # Обновляем роли используя найденный hacker_id и имена ролей
        return await self.hacker_repository.update_hacker_roles_by_names(hacker.id, role_names)
