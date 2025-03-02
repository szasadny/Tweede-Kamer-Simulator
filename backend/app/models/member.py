from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    party_id = Column(Integer, ForeignKey("parties.id"))
    role = Column(String, index=True)
    
    # Political leanings on various dimensions (0-100 scale)
    economic_leaning = Column(Float)  # Left (0) to Right (100)
    social_leaning = Column(Float)    # Progressive (0) to Conservative (100)
    eu_stance = Column(Float)         # Pro-EU (0) to Anti-EU (100)
    
    bio = Column(Text)
    
    # Relationships
    party = relationship("Party", back_populates="members")
    votes = relationship("Vote", back_populates="member")
    debate_entries = relationship("DebateEntry", back_populates="member")
