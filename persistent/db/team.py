from persistent.db.base import Base, WithId
from sqlalchemy import Column, Text, Integer, Boolean, DateTime, Float
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from datetime import datetime


# Таблица для команды
class Team(Base, WithId):
    __tablename__ = "team"

    owner_uuid = Column(UUID(as_uuid=True), nullable=False)
    name = Column(Text, nullable=False)
    size = Column(Integer, nullable=False)
    members = Column(ARRAY(UUID(as_uuid=True)), default=[], nullable=False)
    winner_solutions = Column(ARRAY(UUID(as_uuid=True)), default=[], nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)