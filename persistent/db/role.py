from persistent.db.base import Base, WithMetadata
from sqlalchemy import Column, Text, Integer, Boolean, DateTime, Float, UUID, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime


# Таблица ролей для хакатонов
class Role(Base, WithMetadata):
    __tablename__ = "role"

    name = Column(Text, nullable=False)
