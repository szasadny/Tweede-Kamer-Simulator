from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Member])
def read_members(
    skip: int = 0, 
    limit: int = 100, 
    party_id: int = None,
    db: Session = Depends(get_db)
):
    if party_id:
        members = crud.get_members_by_party(db, party_id=party_id, skip=skip, limit=limit)
    else:
        members = crud.get_members(db, skip=skip, limit=limit)
    return members

@router.post("/", response_model=schemas.Member)
def create_member(
    member: schemas.MemberCreate, 
    db: Session = Depends(get_db)
):
    # Check if party exists
    party = crud.get_party(db, party_id=member.party_id)
    if not party:
        raise HTTPException(status_code=404, detail="Party not found")
    return crud.create_member(db=db, member=member)

@router.get("/{member_id}", response_model=schemas.MemberWithParty)
def read_member(
    member_id: int, 
    db: Session = Depends(get_db)
):
    db_member = crud.get_member(db, member_id=member_id)
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_member

@router.put("/{member_id}", response_model=schemas.Member)
def update_member(
    member_id: int,
    member_data: schemas.MemberCreate,
    db: Session = Depends(get_db)
):
    # Check if party exists
    party = crud.get_party(db, party_id=member_data.party_id)
    if not party:
        raise HTTPException(status_code=404, detail="Party not found")
        
    db_member = crud.update_member(db, member_id=member_id, member_data=member_data)
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_member

@router.delete("/{member_id}")
def delete_member(
    member_id: int,
    db: Session = Depends(get_db)
):
    success = crud.delete_member(db, member_id=member_id)
    if not success:
        raise HTTPException(status_code=404, detail="Member not found")
    return {"detail": "Member successfully deleted"}
