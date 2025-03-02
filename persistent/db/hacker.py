from sqlalchemy.orm import relationship

from persistent.db.base import Base, WithMetadata

from sqlalchemy import Column, Text, Integer, Boolean, DateTime, Float
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from datetime import datetime

from persistent.db.relations import hacker_role_association, hacker_team_association


class Hacker(Base, WithMetadata):
    __tablename__ = "hacker"

    user_id = Column(UUID(as_uuid=True), nullable=False, unique=True)
    name = Column(Text, nullable=False)
    teams = relationship("Team", secondary=hacker_team_association, back_populates="hackers", lazy='subquery')
    roles = relationship("Role", secondary=hacker_role_association, lazy='subquery')



