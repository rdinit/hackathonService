from persistent.db.base import Base, WithId
from sqlalchemy import Column, Text, Integer, Boolean, DateTime, Float, UUID
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime


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
    winners = Column(ARRAY(UUID(as_uuid=True)), default=[], nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
