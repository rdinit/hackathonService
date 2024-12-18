from sqlalchemy.orm import relationship

from persistent.db.base import Base, WithId

from sqlalchemy import Column, Text, Integer, Boolean, DateTime, Float
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from datetime import datetime

from persistent.db.relations import hacker_role_association


class Hacker(Base, WithId):
    __tablename__ = "hacker"

    user_id = Column(UUID(as_uuid=True), nullable=False, unique=True)
    name = Column(Text, nullable=False)
    # teams = Column(ARRAY(UUID(as_uuid=True)), default=[], nullable=False)
    roles = relationship("Role", secondary=hacker_role_association, lazy='subquery')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)



