from sqlalchemy.orm import Session
from app.models.debate import Debate, DebateEntry
from app.schemas.debate import DebateCreate, DebateEntryCreate

def get_debate(db: Session, debate_id: int):
    return db.query(Debate).filter(Debate.id == debate_id).first()

def get_debates(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Debate).offset(skip).limit(limit).all()

def get_debates_by_proposal(db: Session, proposal_id: int):
    return db.query(Debate).filter(Debate.proposal_id == proposal_id).all()

def create_debate(db: Session, debate: DebateCreate):
    db_debate = Debate(**debate.dict())
    db.add(db_debate)
    db.commit()
    db.refresh(db_debate)
    return db_debate

def get_debate_entry(db: Session, entry_id: int):
    return db.query(DebateEntry).filter(DebateEntry.id == entry_id).first()

def get_debate_entries(db: Session, debate_id: int, skip: int = 0, limit: int = 100):
    return db.query(DebateEntry).filter(DebateEntry.debate_id == debate_id).offset(skip).limit(limit).all()

def create_debate_entry(db: Session, entry: DebateEntryCreate):
    db_entry = DebateEntry(**entry.dict())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry
