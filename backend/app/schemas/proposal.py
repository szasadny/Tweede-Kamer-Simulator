from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.proposal import ProposalStatus

class ProposalBase(BaseModel):
    title: str
    content: str
    proposer_id: int

class ProposalCreate(ProposalBase):
    pass

class Proposal(ProposalBase):
    id: int
    status: ProposalStatus
    submitted_date: datetime
    vote_date: Optional[datetime] = None
    
    class Config:
        orm_mode = True

class ProposalDetail(Proposal):
    proposer: Dict[str, Any]
    votes_summary: Optional[Dict[str, int]] = None
    
    class Config:
        orm_mode = True
