from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, ForeignKey, UUID
from persistent.db.base import Base

# Many-to-Many: Hacker <-> Team
hacker_team_association = Table(
    "hacker_team_association",
    Base.metadata,
    Column("hacker_id", UUID(as_uuid=True), ForeignKey("hacker.id"), primary_key=True),
    Column("team_id", UUID(as_uuid=True), ForeignKey("team.id"), primary_key=True),
)

# Establishing Relationships

# Importing all models
from hacker import Hacker
from team import Team
from hackathon import Hackathon
from winner_solution import WinnerSolution

# Adding relationships to models
Hacker.roles = relationship("Role", back_populates="hacker")
Hacker.teams = relationship("Team", secondary=hacker_team_association, back_populates="members")

Team.members = relationship("Hacker", secondary=hacker_team_association, back_populates="teams")
Team.winner_solutions = relationship("WinnerSolution", back_populates="team")

Hackathon.winners = relationship("WinnerSolution", back_populates="hackathon")

WinnerSolution.hackathon = relationship("Hackathon", back_populates="winners")
WinnerSolution.team = relationship("Team", back_populates="winner_solutions")