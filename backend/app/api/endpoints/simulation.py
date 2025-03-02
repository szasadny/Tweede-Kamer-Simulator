from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.ai.simulation import ParliamentSimulation
from app.models.proposal import ProposalStatus

router = APIRouter()

@router.post("/{proposal_id}/start")
async def start_simulation(
    proposal_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # Check if proposal exists
    proposal = crud.get_proposal(db, proposal_id=proposal_id)
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    # Check if proposal is in draft or submitted status
    if proposal.status not in [ProposalStatus.DRAFT, ProposalStatus.SUBMITTED]:
        raise HTTPException(
            status_code=400, 
            detail=f"Simulation can only start for proposals in draft or submitted status, not {proposal.status}"
        )
    
    # Start simulation in the background
    simulation = ParliamentSimulation()
    background_tasks.add_task(
        simulation.run_full_simulation,
        proposal_id=proposal_id,
        db_crud=crud  # Pass the CRUD functions for database operations
    )
    
    # Update proposal status to submitted if it was in draft
    if proposal.status == ProposalStatus.DRAFT:
        crud.update_proposal_status(db, proposal_id=proposal_id, status=ProposalStatus.SUBMITTED)
    
    return {"detail": "Simulation started successfully"}

@router.get("/{proposal_id}/status")
def get_simulation_status(
    proposal_id: int,
    db: Session = Depends(get_db)
):
    # Check if proposal exists
    proposal = crud.get_proposal(db, proposal_id=proposal_id)
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    
    # Get debate info if exists
    debates = crud.get_debates_by_proposal(db, proposal_id=proposal_id)
    
    # Get votes info if exists
    votes = crud.get_votes_by_proposal(db, proposal_id=proposal_id) if proposal.status in [
        ProposalStatus.VOTING, ProposalStatus.PASSED, ProposalStatus.REJECTED
    ] else []
    
    # Get vote summary if in voting or later state
    vote_summary = None
    if proposal.status in [ProposalStatus.VOTING, ProposalStatus.PASSED, ProposalStatus.REJECTED]:
        vote_summary = crud.get_vote_summary(db, proposal_id=proposal_id)
    
    return {
        "proposal_id": proposal_id,
        "status": proposal.status,
        "debates_count": len(debates),
        "votes_count": len(votes),
        "vote_summary": vote_summary.dict() if vote_summary else None
    }
