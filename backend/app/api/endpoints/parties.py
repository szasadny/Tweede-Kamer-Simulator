from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Party])
def read_parties(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    parties = crud.get_parties(db, skip=skip, limit=limit)
    return parties

@router.post("/", response_model=schemas.Party)
def create_party(
    party: schemas.PartyCreate, 
    db: Session = Depends(get_db)
):
    db_party = crud.get_party_by_name(db, name=party.name)
    if db_party:
        raise HTTPException(status_code=400, detail="Party with this name already exists")
    return crud.create_party(db=db, party=party)

@router.get("/{party_id}", response_model=schemas.PartyWithMembers)
def read_party(
    party_id: int, 
    db: Session = Depends(get_db)
):
    db_party = crud.get_party(db, party_id=party_id)
    if db_party is None:
        raise HTTPException(status_code=404, detail="Party not found")
    return db_party

@router.put("/{party_id}", response_model=schemas.Party)
def update_party(
    party_id: int,
    party_data: schemas.PartyCreate,
    db: Session = Depends(get_db)
):
    db_party = crud.update_party(db, party_id=party_id, party_data=party_data)
    if db_party is None:
        raise HTTPException(status_code=404, detail="Party not found")
    return db_party

@router.delete("/{party_id}")
def delete_party(
    party_id: int,
    db: Session = Depends(get_db)
):
    success = crud.delete_party(db, party_id=party_id)
    if not success:
        raise HTTPException(status_code=404, detail="Party not found")
    return {"detail": "Party successfully deleted"}
