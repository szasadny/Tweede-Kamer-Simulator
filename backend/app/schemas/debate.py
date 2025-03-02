from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DebateEntryBase(BaseModel):
    member_id: int
    content: str

class DebateEntryCreate(DebateEntryBase):
    debate_id: int

class DebateEntry(DebateEntryBase):
    id: int
    debate_id: int
    timestamp: datetime
    
    class Config:
        orm_mode = True

class DebateEntryWithMember(DebateEntry):
    member: dict
    
    class Config:
        orm_mode = True

class DebateBase(BaseModel):
    proposal_id: int
    title: str

class DebateCreate(DebateBase):
    pass

class Debate(DebateBase):
    id: int
    date: datetime
    
    class Config:
        orm_mode = True

class DebateDetail(Debate):
    entries: List[DebateEntryWithMember] = []
    proposal: dict
    
    class Config:
        orm_mode = True
