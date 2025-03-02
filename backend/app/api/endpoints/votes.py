from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.models.vote import VoteType
from app.database import get_db

router = APIRouter()

@router.get("/by-proposal/{proposal_id}", response_model=List[schemas.Vote])
def read_votes_by_proposal(
    proposal_id: int, 
    db: Session = Depends(get_db)
):
    # Check if proposal exists
    proposal = crud.get_proposal(db, proposal_id=proposal_id)
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    votes = crud.get_votes_by_proposal(db, proposal_id=proposal_id)
    return votes

@router.post("/", response_model=schemas.Vote)
def create_vote(
    vote: schemas.VoteCreate, 
    db: Session = Depends(get_db)
):
    # Check if proposal exists
    proposal = crud.get_proposal(db, proposal_id=vote.proposal_id)
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    # Check if member exists
    member = crud.get_member(db, member_id=vote.member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    return crud.create_vote(db=db, vote=vote)

@router.get("/summary/{proposal_id}", response_model=schemas.VoteSummary)
def get_vote_summary(
    proposal_id: int, 
    db: Session = Depends(get_db)
):
    # Check if proposal exists
    proposal = crud.get_proposal(db, proposal_id=proposal_id)
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    summary = crud.get_vote_summary(db, proposal_id=proposal_id)
    return summary
