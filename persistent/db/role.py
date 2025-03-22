import enum
from persistent.db.base import Base, WithMetadata
from sqlalchemy import Column, Text, Integer, Boolean, DateTime, Float, UUID, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime
from sqlalchemy.orm import relationship
from persistent.db.relations import hacker_role_association


# Перечисление доступных ролей
class RoleEnum(str, enum.Enum):
    ADMIN = 'Администратор'
    BACKEND = 'Бэкендер'
    FRONTEND = 'Фронтендер'
    ML = 'ML-инженер'
    DESIGNER = 'Дизайнер'
    PM = 'Проект-менеджер'
    QA = 'QA-инженер'
    DEVOPS = 'DevOps-инженер'


# Таблица ролей для хакатонов
class Role(Base, WithMetadata):
    __tablename__ = "role"

    name = Column(Text, nullable=False)
    
    # Отношения
    hackers = relationship("Hacker", secondary=hacker_role_association, back_populates="roles")