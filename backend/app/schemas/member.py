from pydantic import BaseModel
from typing import Optional

class MemberBase(BaseModel):
    name: str
    party_id: int
    role: Optional[str] = None
    economic_leaning: float
    social_leaning: float
    eu_stance: float
    bio: Optional[str] = None

class MemberCreate(MemberBase):
    pass

class MemberBasic(BaseModel):
    id: int
    name: str
    role: Optional[str] = None
    
    class Config:
        orm_mode = True

class Member(MemberBase):
    id: int
    
    class Config:
        orm_mode = True

class MemberWithParty(Member):
    party: "PartyBasic"
    
    class Config:
        orm_mode = True

class PartyBasic(BaseModel):
    id: int
    name: str
    abbreviation: str
    
    class Config:
        orm_mode = True
