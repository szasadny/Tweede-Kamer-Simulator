from pydantic import BaseModel
from app.models.vote import VoteType

class VoteBase(BaseModel):
    proposal_id: int
    member_id: int
    vote: VoteType

class VoteCreate(VoteBase):
    pass

class Vote(VoteBase):
    id: int
    
    class Config:
        orm_mode = True

class VoteSummary(BaseModel):
    total: int
    for_votes: int
    against_votes: int
    abstain_votes: int
    absent_votes: int
    passed: bool
