from sqlalchemy.orm import relationship

from persistent.db.base import Base, WithId
from sqlalchemy import Column, Text, Integer, Boolean, DateTime, Float
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from datetime import datetime

from persistent.db.relations import winner_solution_team_hackathon_association


# Таблица для решений победителя
class WinnerSolution(Base, WithId):
    __tablename__ = "winner_solution"

    hackathon = relationship("Hackathon", secondary=winner_solution_team_hackathon_association, lazy='subquery') #TODO: заменить на one to one
    team = relationship("Team", secondary=winner_solution_team_hackathon_association, lazy='subquery') #TODO: заменить на many to one
    win_money = Column(Float, nullable=False)
    link_to_solution = Column(Text, nullable=False)
    link_to_presentation = Column(Text, nullable=False)
    can_share = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
