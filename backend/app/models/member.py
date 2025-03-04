from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    party_id = Column(Integer, ForeignKey("parties.id"))
    role = Column(String, index=True)

    # Career and education information from opendata.tweedekamer.nl
    career = Column(Text)         # PersoonLoopbaan
    career2 = Column(Text)        # PersoonNevenfunctie
    education = Column(Text)      # PersoonEducation

    # Relationships
    party = relationship("Party", back_populates="members")
    votes = relationship("Vote", back_populates="member")
    debate_entries = relationship("DebateEntry", back_populates="member")
