from persistent.db.base import Base, WithId
from sqlalchemy import Column, Text, Integer, Boolean, DateTime, Float, UUID, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime


# Таблица ролей для хакатонов
class Role(Base, WithId):
    __tablename__ = "role"

    name = Column(Text, nullable=False)
