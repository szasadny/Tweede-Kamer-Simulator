from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from app.database import Base

class VoteType(str, enum.Enum):
    FOR = "for"
    AGAINST = "against"
    ABSTAIN = "abstain"
    ABSENT = "absent"

class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    proposal_id = Column(Integer, ForeignKey("proposals.id"))
    member_id = Column(Integer, ForeignKey("members.id"))
    vote = Column(Enum(VoteType))
    
    # Relationships
    proposal = relationship("Proposal", back_populates="votes")
    member = relationship("Member", back_populates="votes")
