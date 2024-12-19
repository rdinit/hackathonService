from sqlalchemy.orm import relationship

from persistent.db.base import Base, WithId
from sqlalchemy import Column, Text, Integer, Boolean, DateTime, Float, UUID
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime

from persistent.db.relations import winner_solution_team_hackathon_association


# Таблица для хакатона
class Hackathon(Base, WithId):
    __tablename__ = "hackathon"

    name = Column(Text, nullable=False)
    task_description = Column(Text, nullable=False)
    start_of_registration = Column(DateTime, nullable=False)
    end_of_registration = Column(DateTime, nullable=False)
    start_of_hack = Column(DateTime, nullable=False)
    end_of_hack = Column(DateTime, nullable=False)
    amount_money = Column(Float, nullable=False)
    type = Column(Text, nullable=False)  # \"online\" или \"offline\"
    winners = relationship("WinnerSolution", secondary=winner_solution_team_hackathon_association, lazy='subquery')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
