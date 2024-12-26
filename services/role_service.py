from typing import List, Optional

from loguru import logger
from sqlalchemy import UUID

from persistent.db.role import Role
from repository.role_repository import RoleRepository


class RoleService:
    def __init__(self) -> None:
        self.role_repository = RoleRepository()

    async def init_roles(self) -> None:
        """
        Инициализация таблицы Role предопределёнными значениями.
        Если роли уже существуют, инициализация пропускается.
        """
        predefined_roles = ["Бэкенд", "Фронтенд", "ML", "Дизайнер"]

        for role_name in predefined_roles:
            role_exists = await self.role_repository.get_role_by_name(role_name)
            if not role_exists:  # Если роли с таким именем нет
                await self.role_repository.create_role(name=role_name)

    async def get_all_roles(self) -> List[Role]:
        """
        Метод для получения всех ролей.
        """
        roles = await self.role_repository.get_all_roles()
        if not roles:
            logger.warning("Нет ролей в системе.")
        return roles

    async def get_role_by_id(self, role_id: UUID) -> Optional[Role]:
        """
        Получение команды по её идентификатору.
        """
        role = await self.role_repository.get_role_by_id(role_id)
        if not role:
            logger.warning(f"Роль с ID '{role}' не найдена.")
        return role
