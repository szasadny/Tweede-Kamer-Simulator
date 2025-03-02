from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.models.proposal import ProposalStatus
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Proposal])
def read_proposals(
    skip: int = 0, 
    limit: int = 100,
    status: Optional[ProposalStatus] = None,
    db: Session = Depends(get_db)
):
    proposals = crud.get_proposals(db, skip=skip, limit=limit, status=status)
    return proposals

@router.post("/", response_model=schemas.Proposal)
def create_proposal(
    proposal: schemas.ProposalCreate, 
    db: Session = Depends(get_db)
):
    # Check if member exists
    member = crud.get_member(db, member_id=proposal.proposer_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return crud.create_proposal(db=db, proposal=proposal)

@router.get("/{proposal_id}", response_model=schemas.ProposalDetail)
def read_proposal(
    proposal_id: int, 
    db: Session = Depends(get_db)
):
    db_proposal = crud.get_proposal(db, proposal_id=proposal_id)
    if db_proposal is None:
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    # Get the proposer details
    proposer = crud.get_member(db, member_id=db_proposal.proposer_id)
    
    # Get vote summary if in voting or later state
    votes_summary = None
    if db_proposal.status in [ProposalStatus.VOTING, ProposalStatus.PASSED, ProposalStatus.REJECTED]:
        votes_summary = crud.get_vote_summary(db, proposal_id=proposal_id)
        
    result = schemas.ProposalDetail(
        **db_proposal.__dict__,
        proposer={
            "id": proposer.id,
            "name": proposer.name,
            "party": {
                "id": proposer.party.id,
                "name": proposer.party.name,
                "abbreviation": proposer.party.abbreviation
            }
        },
        votes_summary=votes_summary.dict() if votes_summary else None
    )
    
    return result

@router.put("/{proposal_id}/status", response_model=schemas.Proposal)
def update_proposal_status(
    proposal_id: int,
    status: ProposalStatus,
    db: Session = Depends(get_db)
):
    db_proposal = crud.update_proposal_status(db, proposal_id=proposal_id, status=status)
    if db_proposal is None:
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    # If proposal is done with voting, update its final status based on votes
    if status == ProposalStatus.VOTING:
        # When setting to voting, the status remains as voting
        return db_proposal
    
    # When setting to a different status, perform appropriate actions
    if db_proposal.status == ProposalStatus.VOTING:
        vote_summary = crud.get_vote_summary(db, proposal_id=proposal_id)
        if vote_summary.passed:
            db_proposal = crud.update_proposal_status(db, proposal_id=proposal_id, status=ProposalStatus.PASSED)
        else:
            db_proposal = crud.update_proposal_status(db, proposal_id=proposal_id, status=ProposalStatus.REJECTED)
    
    return db_proposal

@router.delete("/{proposal_id}")
def delete_proposal(
    proposal_id: int,
    db: Session = Depends(get_db)
):
    success = crud.delete_proposal(db, proposal_id=proposal_id)
    if not success:
        raise HTTPException(status_code=404, detail="Proposal not found")
    return {"detail": "Proposal successfully deleted"}
