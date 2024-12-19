from typing import List, Optional
from loguru import logger

from persistent.db.team import Team
from repository.team_repository import TeamRepository


class TeamService:
    def __init__(self) -> None:
        self.team_repository = TeamRepository()

    async def create_team(self, owner_uuid: str, name: str, size: int) -> Team:
        """
        Создание новой команды.
        """
        team_exists = await self.team_repository.get_team_by_name(name)
        if team_exists:
            logger.warning(f"Команда с именем '{name}' уже существует.")
            raise ValueError(f"Команда с именем '{name}' уже существует.")

        new_team = await self.team_repository.create_team(
            owner_uuid=owner_uuid,
            name=name,
            size=size,
        )
        logger.info(f"Команда '{name}' успешно создана.")
        return new_team

    async def get_all_teams(self) -> List[Team]:
        """
        Получение списка всех команд.
        """
        teams = await self.team_repository.get_all_teams()
        if not teams:
            logger.warning("Нет зарегистрированных команд.")
        return teams

    async def get_team_by_id(self, team_id: str) -> Optional[Team]:
        """
        Получение команды по её идентификатору.
        """
        team = await self.team_repository.get_team_by_id(team_id)
        if not team:
            logger.warning(f"Команда с ID '{team_id}' не найдена.")
        return team

    async def add_hacker_to_team(self, team_id: str, hacker_id: str) -> None:
        """
        Добавление участника в команду.
        """
        team = await self.team_repository.get_team_by_id(team_id)
        if not team:
            logger.error(f"Команда с ID '{team_id}' не найдена.")
            raise ValueError(f"Команда с ID '{team_id}' не найдена.")

        if len(team.hackers) >= team.size:
            logger.error(f"Команда '{team.name}' уже заполнена.")
            raise ValueError(f"Команда '{team.name}' уже заполнена.")

        await self.team_repository.add_hacker_to_team(team_id, hacker_id)
        logger.info(f"Участник с ID '{hacker_id}' добавлен в команду '{team.name}'.")

    async def remove_hacker_from_team(self, team_id: str, hacker_id: str) -> None:
        """
        Удаление участника из команды.
        """
        team = await self.team_repository.get_team_by_id(team_id)
        if not team:
            logger.error(f"Команда с ID '{team_id}' не найдена.")
            raise ValueError(f"Команда с ID '{team_id}' не найдена.")

        await self.team_repository.remove_hacker_from_team(team_id, hacker_id)
        logger.info(f"Участник с ID '{hacker_id}' удалён из команды '{team.name}'.")

    async def delete_team(self, team_id: str) -> None:
        """
        Удаление команды.
        """
        team = await self.team_repository.get_team_by_id(team_id)
        if not team:
            logger.error(f"Команда с ID '{team_id}' не найдена.")
            raise ValueError(f"Команда с ID '{team_id}' не найдена.")

        await self.team_repository.delete_team(team_id)
        logger.info(f"Команда '{team.name}' удалена.")
