from pydantic import BaseModel
from typing import Optional, List

class PartyBase(BaseModel):
    name: str
    abbreviation: str

class PartyCreate(PartyBase):
    pass

class Party(PartyBase):
    id: int
    
    class Config:
        orm_mode = True

class PartyWithMembers(Party):
    members: List["MemberBasic"] = []
    
    class Config:
        orm_mode = True
