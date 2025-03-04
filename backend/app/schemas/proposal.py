from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.proposal import ProposalStatus

class ProposalBase(BaseModel):
    title: str
    content: str

class ProposalCreate(ProposalBase):
    pass

class Proposal(ProposalBase):
    id: int
    status: ProposalStatus
    
    class Config:
        orm_mode = True

class ProposalDetail(Proposal):
    votes_summary: Optional[Dict[str, int]] = None
    
    class Config:
        orm_mode = True
