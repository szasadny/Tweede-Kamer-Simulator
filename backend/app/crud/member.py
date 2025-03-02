from sqlalchemy.orm import Session
from app.models.member import Member
from app.schemas.member import MemberCreate

def get_member(db: Session, member_id: int):
    return db.query(Member).filter(Member.id == member_id).first()

def get_members(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Member).offset(skip).limit(limit).all()

def get_members_by_party(db: Session, party_id: int, skip: int = 0, limit: int = 100):
    return db.query(Member).filter(Member.party_id == party_id).offset(skip).limit(limit).all()

def create_member(db: Session, member: MemberCreate):
    db_member = Member(**member.dict())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

def update_member(db: Session, member_id: int, member_data):
    db_member = db.query(Member).filter(Member.id == member_id).first()
    if db_member:
        for key, value in member_data.dict(exclude_unset=True).items():
            setattr(db_member, key, value)
        db.commit()
        db.refresh(db_member)
    return db_member

def delete_member(db: Session, member_id: int):
    db_member = db.query(Member).filter(Member.id == member_id).first()
    if db_member:
        db.delete(db_member)
        db.commit()
        return True
    return False
