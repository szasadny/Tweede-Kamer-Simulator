from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

from app.database import Base

class ProposalStatus(str, enum.Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    DEBATING = "debating"
    VOTING = "voting"
    PASSED = "passed"
    REJECTED = "rejected"

class Proposal(Base):
    __tablename__ = "proposals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    proposer_id = Column(Integer, ForeignKey("members.id"))
    status = Column(Enum(ProposalStatus), default=ProposalStatus.DRAFT)
    submitted_date = Column(DateTime, default=datetime.utcnow)
    vote_date = Column(DateTime, nullable=True)
    
    # Relationships
    proposer = relationship("Member")
    debates = relationship("Debate", back_populates="proposal")
    votes = relationship("Vote", back_populates="proposal")
