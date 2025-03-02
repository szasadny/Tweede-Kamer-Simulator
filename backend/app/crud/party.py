from sqlalchemy.orm import Session
from app.models.party import Party
from app.schemas.party import PartyCreate

def get_party(db: Session, party_id: int):
    return db.query(Party).filter(Party.id == party_id).first()

def get_party_by_name(db: Session, name: str):
    return db.query(Party).filter(Party.name == name).first()

def get_parties(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Party).offset(skip).limit(limit).all()

def create_party(db: Session, party: PartyCreate):
    db_party = Party(**party.dict())
    db.add(db_party)
    db.commit()
    db.refresh(db_party)
    return db_party

def update_party(db: Session, party_id: int, party_data):
    db_party = db.query(Party).filter(Party.id == party_id).first()
    if db_party:
        for key, value in party_data.dict(exclude_unset=True).items():
            setattr(db_party, key, value)
        db.commit()
        db.refresh(db_party)
    return db_party

def delete_party(db: Session, party_id: int):
    db_party = db.query(Party).filter(Party.id == party_id).first()
    if db_party:
        db.delete(db_party)
        db.commit()
        return True
    return False
