from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.vote import Vote, VoteType
from app.schemas.vote import VoteCreate, VoteSummary

def get_vote(db: Session, vote_id: int):
    return db.query(Vote).filter(Vote.id == vote_id).first()

def get_vote_by_member_proposal(db: Session, member_id: int, proposal_id: int):
    return db.query(Vote).filter(
        Vote.member_id == member_id,
        Vote.proposal_id == proposal_id
    ).first()

def get_votes_by_proposal(db: Session, proposal_id: int):
    return db.query(Vote).filter(Vote.proposal_id == proposal_id).all()

def create_vote(db: Session, vote: VoteCreate):
    # Check if vote exists already and update if so
    db_vote = get_vote_by_member_proposal(db, vote.member_id, vote.proposal_id)
    if db_vote:
        db_vote.vote = vote.vote
        db.commit()
        db.refresh(db_vote)
        return db_vote
    
    # Otherwise create new vote
    db_vote = Vote(**vote.dict())
    db.add(db_vote)
    db.commit()
    db.refresh(db_vote)
    return db_vote

def get_vote_summary(db: Session, proposal_id: int) -> VoteSummary:
    votes = get_votes_by_proposal(db, proposal_id)
    
    total = len(votes)
    for_votes = sum(1 for v in votes if v.vote == VoteType.FOR)
    against_votes = sum(1 for v in votes if v.vote == VoteType.AGAINST)
    abstain_votes = sum(1 for v in votes if v.vote == VoteType.ABSTAIN)
    absent_votes = sum(1 for v in votes if v.vote == VoteType.ABSENT)
    
    # Simple majority rule
    passed = for_votes > against_votes
    
    return VoteSummary(
        total=total,
        for_votes=for_votes,
        against_votes=against_votes,
        abstain_votes=abstain_votes,
        absent_votes=absent_votes,
        passed=passed
    )
