from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, ForeignKey, UUID
from persistent.db.base import Base

# Many-to-Many: Hacker <-> Role
hacker_role_association = Table(
    "hacker_role_association",
    Base.metadata,
    Column("hacker_id", UUID(as_uuid=True), ForeignKey("hacker.id"), primary_key=True),
    Column("role_id", UUID(as_uuid=True), ForeignKey("role.id"), primary_key=True),
)

# Many-to-Many: Hacker <-> Team
hacker_team_association = Table(
    "hacker_team_association",
    Base.metadata,
    Column("hacker_id", UUID(as_uuid=True), ForeignKey("hacker.id"), primary_key=True),
    Column("team_id", UUID(as_uuid=True), ForeignKey("team.id"), primary_key=True),
)