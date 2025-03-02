from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Debate])
def read_debates(
    skip: int = 0, 
    limit: int = 100,
    proposal_id: int = None, 
    db: Session = Depends(get_db)
):
    if proposal_id:
        debates = crud.get_debates_by_proposal(db, proposal_id=proposal_id)
    else:
        debates = crud.get_debates(db, skip=skip, limit=limit)
    return debates

@router.post("/", response_model=schemas.Debate)
def create_debate(
    debate: schemas.DebateCreate, 
    db: Session = Depends(get_db)
):
    # Check if proposal exists
    proposal = crud.get_proposal(db, proposal_id=debate.proposal_id)
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    return crud.create_debate(db=db, debate=debate)

@router.get("/{debate_id}", response_model=schemas.DebateDetail)
def read_debate(
    debate_id: int, 
    db: Session = Depends(get_db)
):
    db_debate = crud.get_debate(db, debate_id=debate_id)
    if db_debate is None:
        raise HTTPException(status_code=404, detail="Debate not found")
    return db_debate

@router.post("/entries/", response_model=schemas.DebateEntry)
def create_debate_entry(
    entry: schemas.DebateEntryCreate, 
    db: Session = Depends(get_db)
):
    # Check if debate exists
    debate = crud.get_debate(db, debate_id=entry.debate_id)
    if not debate:
        raise HTTPException(status_code=404, detail="Debate not found")
    
    # Check if member exists
    member = crud.get_member(db, member_id=entry.member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    return crud.create_debate_entry(db=db, entry=entry)

@router.get("/entries/{entry_id}", response_model=schemas.DebateEntryWithMember)
def read_debate_entry(
    entry_id: int, 
    db: Session = Depends(get_db)
):
    db_entry = crud.get_debate_entry(db, entry_id=entry_id)
    if db_entry is None:
        raise HTTPException(status_code=404, detail="Debate entry not found")
    return db_entry
