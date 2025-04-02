from datetime import datetime
from typing import cast, List, Optional

from loguru import logger
from sqlalchemy.exc import IntegrityError

from infrastructure.db.connection import pg_connection
from persistent.db.hacker import Hacker
from persistent.db.role import Role, RoleEnum
from sqlalchemy import ColumnElement, select, update, delete, insert, UUID, String, Table
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker


class HackerRepository:
    def __init__(self) -> None:
        self._sessionmaker = pg_connection()

    async def get_all_hackers(self) -> List[Hacker]:
        """
        Метод для получения всех хакеров.
        Возвращает список хакеров из базы данных.
        """
        stmt = select(Hacker)

        async with self._sessionmaker() as session:
            resp = await session.execute(stmt)

            rows = resp.fetchall()  # Извлекаем все строки
            hackers = [row[0] for row in rows]  # Преобразуем их в список объектов Hacker
            return hackers

    async def upsert_hacker(self, user_id: UUID, name: str) -> Optional[UUID]:
        """
        Создание или обновление хакера без ролей
        """
        try:
            async with self._sessionmaker() as session:
                async with session.begin():
                    # Проверяем существующего хакера
                    get_stmt = select(Hacker).where(Hacker.user_id == user_id)
                    result = await session.execute(get_stmt)
                    existing_hacker = result.scalar_one_or_none()
                    
                    if existing_hacker:
                        # Если хакер существует, обновляем его
                        update_stmt = update(Hacker).where(
                            Hacker.id == existing_hacker.id
                        ).values(
                            name=name,
                            updated_at=datetime.utcnow()
                        )
                        await session.execute(update_stmt)
                        return existing_hacker.id
                    else:
                        # Если хакера нет, создаем нового
                        new_hacker = Hacker(
                            user_id=user_id,
                            name=name,
                            created_at=datetime.utcnow(),
                            updated_at=datetime.utcnow()
                        )
                        session.add(new_hacker)
                        await session.flush()
                        return new_hacker.id
                    
        except Exception as e:
            logger.error(f"Error in upsert_hacker: {e}")
            return None

    async def update_hacker_roles(self, hacker_id: UUID, role_ids: List[UUID]) -> bool:
        """
        Обновление ролей хакера по их ID из списка доступных ролей.
        """
        try:
            async with self._sessionmaker() as session:
                async with session.begin():
                    # Получаем хакера
                    hacker_stmt = select(Hacker).where(cast("ColumnElement[bool]", Hacker.id == hacker_id)).limit(1)
                    hacker_result = await session.execute(hacker_stmt)
                    hacker_row = hacker_result.fetchone()
                    
                    if not hacker_row:
                        return False
                        
                    hacker = hacker_row[0]
                        
                    # Получаем роли по указанным ID
                    role_stmt = select(Role).where(Role.id.in_(role_ids))
                    role_result = await session.execute(role_stmt)
                    roles = role_result.scalars().all()
                    
                    # Устанавливаем новые роли для хакера
                    hacker.roles = roles
                    
                    return True
                    
        except IntegrityError as e:
            logger.error(f"IntegrityError in update_hacker_roles: {e}")
            return False
        except Exception as e:
            logger.error(f"Error in update_hacker_roles: {e}")
            return False

    async def get_hacker_by_id(self, hacker_id: UUID) -> Optional[Hacker]:
        """
        Получение хакера по ID.
        """
        stmt = select(Hacker).where(cast("ColumnElement[bool]", Hacker.id == hacker_id)).limit(1)

        async with self._sessionmaker() as session:
            resp = await session.execute(stmt)
            row = resp.fetchone()
            return row[0] if row else None

    async def get_hacker_by_user_id(self, user_id: UUID) -> Optional[Hacker]:
        """
        Получение хакера по user_id.
        """
        stmt = select(Hacker).where(cast("ColumnElement[bool]", Hacker.user_id == user_id)).limit(1)

        async with self._sessionmaker() as session:
            resp = await session.execute(stmt)
            row = resp.fetchone()
            return row[0] if row else None

    async def update_hacker_roles_by_names(self, hacker_id: UUID, role_names: List[str]) -> bool:
        """
        Обновление ролей хакера по их именам из списка доступных ролей.
        """
        try:
            async with self._sessionmaker() as session:
                async with session.begin():
                    # Получаем хакера
                    hacker_stmt = select(Hacker).where(cast("ColumnElement[bool]", Hacker.id == hacker_id)).limit(1)
                    hacker_result = await session.execute(hacker_stmt)
                    hacker_row = hacker_result.fetchone()
                    
                    if not hacker_row:
                        return False
                        
                    hacker = hacker_row[0]
                        
                    # Получаем роли по их именам
                    role_stmt = select(Role).where(Role.name.in_(role_names))
                    role_result = await session.execute(role_stmt)
                    roles = role_result.scalars().all()
                    
                    # Проверяем, найдены ли все роли
                    if len(roles) != len(role_names):
                        logger.warning(f"Не все роли найдены. Запрошено: {role_names}, найдено: {[role.name for role in roles]}")
                    
                    # Устанавливаем новые роли для хакера
                    hacker.roles = roles
                    
                    return True
                    
        except IntegrityError as e:
            logger.error(f"IntegrityError in update_hacker_roles_by_names: {e}")
            return False
        except Exception as e:
            logger.error(f"Error in update_hacker_roles_by_names: {e}")
            return False
