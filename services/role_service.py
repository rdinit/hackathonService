from loguru import logger
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