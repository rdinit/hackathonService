from typing import List, Optional, Tuple
from uuid import UUID
from loguru import logger

from persistent.db.role import Role, RoleEnum
from repository.role_repository import RoleRepository


class RoleService:
    def __init__(self) -> None:
        self.role_repository = RoleRepository()

    async def get_all_roles(self) -> List[Role]:
        """
        Возвращает все роли.
        """
        roles = await self.role_repository.get_all_roles()
        
        return roles

    async def init_roles(self) -> None:
        """
        Инициализирует роли в системе на основе перечисления RoleEnum.
        """
        for role_enum in RoleEnum:
            role_name = role_enum.value
            role_id = await self.role_repository.upsert_role(role_name)

    async def get_role_by_id(self, role_id: UUID) -> Tuple[Role, bool]:
        """
        Получение роли по её идентификатору.

        :returns False Роль не найдена
        """
        role = await self.role_repository.get_role_by_id(role_id)

        if not role:
            return None, False

        return role, True

    async def upsert_role(self, role_name: str) -> Tuple[UUID, int]:
        """
        Создание или обновление роли.

        :returns -1 Недопустимое имя роли
        :returns -2 Ошибка при создании роли
        """
        valid_roles = [role.value for role in RoleEnum]
        if role_name not in valid_roles:
            logger.warning(f"Попытка создать недопустимую роль: '{role_name}'")
            return None, -1

        role_id = await self.role_repository.upsert_role(role_name)
        if not role_id:
            return None, -2

        return role_id, 1