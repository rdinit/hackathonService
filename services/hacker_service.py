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

    async def upsert_hacker(self, user_id: UUID, name: str) -> UUID:
        """
        Создаёт или обновляет хакатонщика.
        """
        hacker_id = await self.hacker_repository.upsert_hacker(user_id, name)

        return hacker_id

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
