from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base

class Party(Base):
    __tablename__ = "parties"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    abbreviation = Column(String, unique=True, index=True)

    # Relationships
    members = relationship("Member", back_populates="party")
