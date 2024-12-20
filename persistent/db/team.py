from sqlalchemy.orm import relationship

from persistent.db.base import Base, WithId
from sqlalchemy import Column, Text, Integer, Boolean, DateTime, Float
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from datetime import datetime

from persistent.db.relations import hacker_team_association


# Таблица для команды
class Team(Base, WithId):
    __tablename__ = "team"

    owner_id = Column(UUID(as_uuid=True), nullable=False)
    name = Column(Text, nullable=False)
    size = Column(Integer, nullable=False)
    hackers = relationship("Hacker", secondary=hacker_team_association, back_populates="teams", lazy='subquery')
    winner_solutions = relationship("WinnerSolution", back_populates="team", lazy='subquery')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)