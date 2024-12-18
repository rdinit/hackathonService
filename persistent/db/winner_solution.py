from persistent.db.base import Base, WithId
from sqlalchemy import Column, Text, Integer, Boolean, DateTime, Float
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from datetime import datetime


# Таблица для решений победителя
class WinnerSolution(Base, WithId):
    __tablename__ = "winner_solution"

    hackathon = Column(UUID(as_uuid=True), nullable=False)
    team = Column(UUID(as_uuid=True), nullable=False)
    win_money = Column(Float, nullable=False)
    link_to_solution = Column(Text, nullable=False)
    link_to_presentation = Column(Text, nullable=False)
    can_share = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
