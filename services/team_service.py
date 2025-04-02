from datetime import datetime
from typing import List, Optional, Tuple
from loguru import logger
from sqlalchemy import UUID

from infrastructure.db.connection import pg_connection
from persistent.db.team import Team
from repository.hacker_repository import HackerRepository
from repository.team_repository import TeamRepository


class TeamService:
    def __init__(self) -> None:
        self.team_repository = TeamRepository()
        self.hacker_repository = HackerRepository()

    async def get_all_teams(self) -> List[Team]:
        """
        Возвращает все команды.
        """
        teams = await self.team_repository.get_all_teams()

        if not teams:
            logger.warning("Команды не найдены.")
        return teams

    async def create_team(self, owner_id: UUID, name: str, max_size: int) -> Tuple[UUID, int]:
        """
        Создаёт новую команду.

        :returns -1 max_size должен быть больше 0
        :returns -2 Команда с таким владельцем и названием уже существует
        """
        if max_size <= 0:
            return None, -1

        new_team_id = await self.team_repository.create_team(
            owner_id=owner_id,
            name=name,
            max_size=max_size,
        )

        if not new_team_id:
            return None, -2

        await self.add_hacker_to_team(new_team_id, owner_id)

        return new_team_id, 1

    async def get_team_by_id(self, team_id: UUID) -> Tuple[Team, bool]:
        """
        Получение команды по её идентификатору.

        :returns False Команда не найдена
        """
        team = await self.team_repository.get_team_by_id(team_id)

        if not team:
            return None, False

        return team, True

    async def add_hacker_to_team(self, team_id: UUID, hacker_id: UUID) -> Tuple[Team, int]:
        """
        Добавление участника в команду.

        :returns -1 Хакер не найден
        :returns -2 Команда не найдена
        :returns -3 Команда уже заполнена
        """

        hacker = await self.hacker_repository.get_hacker_by_id(hacker_id)

        if not hacker:
            return None, -1

        team, ok = await self.team_repository.add_hacker_to_team(team_id, hacker)

        if ok == -1:
            return None, -2

        if ok == -2:
            return None, -3
        
        return team, 1

    async def get_teams_by_user_id(self, user_id: UUID) -> List[Team]:
        """
        Получение всех команд пользователя.
        
        Находит команды, в которых участвует пользователь с указанным user_id.
        """
        teams = await self.team_repository.get_teams_by_user_id(user_id)
        
        if not teams:
            logger.info(f"Команды не найдены для пользователя с user_id={user_id}")
            
        return teams

