from sqlalchemy.orm import relationship, mapped_column

from persistent.db.base import Base, WithMetadata
from sqlalchemy import Column, Text, Integer, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from datetime import datetime


# Таблица для решений победителя
class WinnerSolution(Base, WithMetadata):
    __tablename__ = "winner_solution"

    hackathon_id = mapped_column(ForeignKey("hackathon.id"))
    hackathon = relationship("Hackathon", back_populates="winner_solutions", lazy='subquery')
    team_id = mapped_column(ForeignKey("team.id"))
    team = relationship("Team", back_populates="winner_solutions", lazy='subquery')
    win_money = Column(Float, nullable=False)
    link_to_solution = Column(Text, nullable=False)
    link_to_presentation = Column(Text, nullable=False)
    can_share = Column(Boolean, default=True, nullable=False)
