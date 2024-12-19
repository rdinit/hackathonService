from uuid import UUID
from datetime import datetime
from typing import List, Optional

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
        hackers = await self.hacker_repository.get_all_hackers()
        return hackers

    async def create_hacker(self, user_id: UUID, name: str) -> UUID:
        """
        Метод для создания нового хакера.
        """
        #TODO: добавить проверку что хакера с таким user_id ещё нет
        hacker_id = await self.hacker_repository.add_hacker(user_id, name)
        return hacker_id

    async def get_hacker_by_id(self, hacker_id: UUID) -> Optional[Hacker]:
        """
        Метод для поиска хакера по его уникальному ID.
        """
        hacker = await self.hacker_repository.get_hacker_by_id(hacker_id)
        return hacker

    async def get_hacker_by_user_id(self, user_id: UUID) -> Optional[Hacker]:
        """
        Метод для поиска хакера по его user_id (UUID).
        """
        hacker = await self.hacker_repository.get_hacker_by_user_id(user_id)
        return hacker

    async def add_roles_to_hacker(self, hacker_id: UUID, roles: List[Role]) -> None:
        """
        Метод для добавления ролей хакеру.
        В SQLAlchemy это обновит связанные записи в таблице через промежуточную таблицу.
        """
        hacker = await self.hacker_repository.get_hacker_by_id(hacker_id)

        if hacker:
            # Добавляем роли как элементы списка
            hacker.roles.extend(roles)  # Данный шаг добавляет роли в список

            #TODO добавить проверку, чтобы не было двух одинаковых ролей у одного хакера

            # Обновляем поле updated_at
            hacker.updated_at = datetime.utcnow()

            # Сохраняем изменения в базе данных
            async with self._sessionmaker() as session:
                # Для того чтобы изменения были зафиксированы в базе данных
                session.add(hacker)  # Добавляем объект в сессию
                await session.commit()  # Совершаем коммит

    async def update_hacker_roles(self, hacker_id: UUID, roles: List[Role]) -> None:
        """
        Метод для обновления ролей хакера.
        В SQLAlchemy это обновит связанные записи в таблице через промежуточную таблицу.
        """
        hacker = await self.hacker_repository.get_hacker_by_id(hacker_id)

        if hacker:
            # Добавляем роли как элементы списка
            hacker.roles = roles  # Данный шаг добавляет роли в список

            # Обновляем поле updated_at
            hacker.updated_at = datetime.utcnow()

            # Сохраняем изменения в базе данных
            async with self._sessionmaker() as session:
                # Для того чтобы изменения были зафиксированы в базе данных
                session.add(hacker)  # Добавляем объект в сессию
                await session.commit()  # Совершаем коммит
