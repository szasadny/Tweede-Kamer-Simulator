from app.crud.party import get_party, get_parties, create_party, update_party, delete_party
from app.crud.member import get_member, get_members, get_members_by_party, create_member, update_member, delete_member
from app.crud.proposal import get_proposal, get_proposals, create_proposal, update_proposal, update_proposal_status, delete_proposal
from app.crud.debate import get_debate, get_debates, get_debates_by_proposal, create_debate, get_debate_entry, get_debate_entries, create_debate_entry
from app.crud.vote import get_vote, get_votes_by_proposal, create_vote, get_vote_summary
