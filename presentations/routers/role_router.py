from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from loguru import logger

from services.role_service import RoleService

role_service = RoleService()

role_router = APIRouter(
    prefix="/role",
    tags=["Roles"],
    responses={404: {"description": "Not Found"}},
)


class RoleDto(BaseModel):
    id: UUID
    name: str


class RoleGetAllResponse(BaseModel):
    roles: List[RoleDto]


class RoleCreatePostRequest(BaseModel):
    name: str


class RoleCreatePostResponse(BaseModel):
    id: UUID


class RoleGetByIdResponse(BaseModel):
    id: UUID
    name: str


@role_router.get("/", response_model=RoleGetAllResponse)
async def get_all_roles():
    """
    Получить список всех ролей.
    """
    logger.info("Запрос на получение списка всех ролей.")
    try:
        roles = await role_service.get_all_roles()
        logger.info(f"Получено {len(roles)} ролей.")
        return RoleGetAllResponse(
            roles=[
                RoleDto(
                    id=role.id,
                    name=role.name,
                )
                for role in roles
            ]
        )
    except Exception as e:
        logger.exception("Ошибка при получении списка ролей.")
        raise HTTPException(status_code=400, detail="Не удалось получить список ролей.")


@role_router.get("/{role_id}", response_model=RoleGetByIdResponse)
async def get_role_by_id(role_id: UUID):
    """
    Получить информацию о роли по ID.
    """
    logger.info(f"Запрос на получение информации о роли с ID {role_id}.")
    try:
        role = await role_service.get_role_by_id(role_id)
        if not role:
            logger.warning(f"Роль с ID {role_id} не найдена.")
            raise HTTPException(status_code=404, detail="Роль не найдена")

        logger.info(f"Роль с ID {role_id} найдена: {role.name}.")
        return RoleGetByIdResponse(
            id=role.id,
            name=role.name,
        )
    except Exception as e:
        logger.exception(f"Ошибка при получении информации о роли с ID {role_id}.")
        raise HTTPException(status_code=400, detail="Не удалось получить информацию о роли.")
