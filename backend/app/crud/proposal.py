from sqlalchemy.orm import Session
from app.models.proposal import Proposal, ProposalStatus
from app.schemas.proposal import ProposalCreate
from datetime import datetime

def get_proposal(db: Session, proposal_id: int):
    return db.query(Proposal).filter(Proposal.id == proposal_id).first()

def get_proposals(db: Session, skip: int = 0, limit: int = 100, status: ProposalStatus = None):
    query = db.query(Proposal)
    if status:
        query = query.filter(Proposal.status == status)
    return query.offset(skip).limit(limit).all()

def create_proposal(db: Session, proposal: ProposalCreate):
    db_proposal = Proposal(**proposal.dict(), status=ProposalStatus.DRAFT)
    db.add(db_proposal)
    db.commit()
    db.refresh(db_proposal)
    return db_proposal

def update_proposal_status(db: Session, proposal_id: int, status: ProposalStatus):
    db_proposal = db.query(Proposal).filter(Proposal.id == proposal_id).first()
    if db_proposal:
        db_proposal.status = status
        if status == ProposalStatus.VOTING:
            db_proposal.vote_date = datetime.utcnow()
        db.commit()
        db.refresh(db_proposal)
    return db_proposal

def update_proposal(db: Session, proposal_id: int, proposal_data):
    db_proposal = db.query(Proposal).filter(Proposal.id == proposal_id).first()
    if db_proposal:
        for key, value in proposal_data.dict(exclude_unset=True).items():
            setattr(db_proposal, key, value)
        db.commit()
        db.refresh(db_proposal)
    return db_proposal

def delete_proposal(db: Session, proposal_id: int):
    db_proposal = db.query(Proposal).filter(Proposal.id == proposal_id).first()
    if db_proposal:
        db.delete(db_proposal)
        db.commit()
        return True
    return False
