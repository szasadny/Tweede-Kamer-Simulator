from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base

class Debate(Base):
    __tablename__ = "debates"

    id = Column(Integer, primary_key=True, index=True)
    proposal_id = Column(Integer, ForeignKey("proposals.id"))
    title = Column(String, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    proposal = relationship("Proposal", back_populates="debates")
    entries = relationship("DebateEntry", back_populates="debate")

class DebateEntry(Base):
    __tablename__ = "debate_entries"

    id = Column(Integer, primary_key=True, index=True)
    debate_id = Column(Integer, ForeignKey("debates.id"))
    member_id = Column(Integer, ForeignKey("members.id"))
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    debate = relationship("Debate", back_populates="entries")
    member = relationship("Member", back_populates="debate_entries")
