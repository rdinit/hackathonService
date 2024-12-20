from datetime import datetime
from typing import List, Optional
from loguru import logger
from sqlalchemy import UUID

from infrastructure.db.connection import pg_connection
from persistent.db.team import Team
from repository.hacker_repository import HackerRepository
from repository.team_repository import TeamRepository


class TeamService:
    def __init__(self) -> None:
        self._sessionmaker = pg_connection()
        self.team_repository = TeamRepository()
        self.hacker_repository = HackerRepository()

    async def get_all_teams(self) -> List[Team]:
        """
        Получение списка всех команд.
        """
        teams = await self.team_repository.get_all_teams()

        if not teams:
            logger.warning("Команды не найдены.")
        return teams

    async def create_team(self, owner_id: UUID, name: str, size: int) -> UUID:
        """
        Создание новой команды.
        """
        new_team_id = await self.team_repository.create_team(
            owner_id=owner_id,
            name=name,
            size=size,
        )
        logger.info(f"Команда '{name}' успешно создана.")
        return new_team_id

    async def get_team_by_id(self, team_id: UUID) -> Optional[Team]:
        """
        Получение команды по её идентификатору.
        """
        team = await self.team_repository.get_team_by_id(team_id)
        if not team:
            logger.warning(f"Команда с ID '{team_id}' не найдена.")
        return team

    async def add_hacker_to_team(self, team_id: UUID, hacker_id: UUID) -> None:
        """
        Добавление участника в команду.
        """
        team = await self.team_repository.get_team_by_id(team_id)
        hacker = await self.hacker_repository.get_hacker_by_id(hacker_id)
        if not team:
            raise ValueError(f"Команда с ID '{team_id}' не найдена.")

        if len(team.hackers) >= team.size:
            raise ValueError(f"Команда '{team.name}' уже заполнена.")

        if not hacker:
            raise ValueError(f"Хакер с ID '{hacker_id}' не найдена.")

        # Добавляем роли как элементы списка
        team.hackers.append(hacker)  # Данный шаг добавляет роли в список

        # Обновляем поле updated_at
        team.updated_at = datetime.utcnow()
        hacker.updated_at = datetime.utcnow()

        # Сохраняем изменения в базе данных
        async with self._sessionmaker() as session:
            # Для того чтобы изменения были зафиксированы в базе данных
            session.add(team)
            session.add(hacker)  # Добавляем объект в сессию
            await session.commit()  # Совершаем коммит
