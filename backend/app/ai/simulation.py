from typing import List, Dict, Any
import asyncio
from app.ai.agents import ParliamentaryAgent
from app.models.vote import VoteType
from app.models.proposal import ProposalStatus

class ParliamentSimulation:
    def __init__(self, agent: ParliamentaryAgent = None):
        self.agent = agent or ParliamentaryAgent()
    
    async def simulate_debate(self, proposal_data: Dict[Any, Any], members: List[Dict[Any, Any]], 
                             debate_id: int, db_crud):
        """
        Simulate a debate on a proposal among parliament members
        """
        # Limit the number of members participating in the debate for efficiency
        participating_members = members[:15]  # Take only some members
        
        debate_entries = []
        
        # Generate debate entries for each participating member
        for member in participating_members:
            try:
                debate_content = await self.agent.generate_debate_entry(member, proposal_data)
                
                # Create debate entry in the database
                entry = {
                    "debate_id": debate_id,
                    "member_id": member["id"],
                    "content": debate_content
                }
                
                db_entry = await db_crud.create_debate_entry(entry)
                debate_entries.append(db_entry)
                
                # Small delay to avoid rate limiting
                await asyncio.sleep(1)
                
            except Exception as e:
                print(f"Error generating debate entry for member {member['name']}: {str(e)}")
        
        return debate_entries
    
    async def simulate_voting(self, proposal_id: int, proposal_data: Dict[Any, Any], 
                             members: List[Dict[Any, Any]], debate_summary: str, db_crud):
        """
        Simulate voting on a proposal among parliament members
        """
        votes = []
        
        # Generate votes for each member
        for member in members:
            try:
                vote_type = await self.agent.generate_vote(member, proposal_data, debate_summary)
                
                # Create vote in the database
                vote = {
                    "proposal_id": proposal_id,
                    "member_id": member["id"],
                    "vote": vote_type
                }
                
                db_vote = await db_crud.create_vote(vote)
                votes.append(db_vote)
                
                # Small delay to avoid rate limiting
                await asyncio.sleep(0.5)
                
            except Exception as e:
                print(f"Error generating vote for member {member['name']}: {str(e)}")
                # Default to absent if there's an error
                vote = {
                    "proposal_id": proposal_id,
                    "member_id": member["id"],
                    "vote": VoteType.ABSENT
                }
                db_vote = await db_crud.create_vote(vote)
                votes.append(db_vote)
        
        # Determine outcome
        for_votes = sum(1 for v in votes if v.vote == VoteType.FOR)
        against_votes = sum(1 for v in votes if v.vote == VoteType.AGAINST)
        
        if for_votes > against_votes:
            await db_crud.update_proposal_status(proposal_id, ProposalStatus.PASSED)
        else:
            await db_crud.update_proposal_status(proposal_id, ProposalStatus.REJECTED)
        
        return votes
    
    async def run_full_simulation(self, proposal_id: int, db_crud):
        """
        Run a full simulation of the parliamentary process for a proposal
        """
        # Get proposal data
        proposal = await db_crud.get_proposal(proposal_id)
        if not proposal:
            raise ValueError(f"Proposal with id {proposal_id} not found")
        
        # Get all members
        members = await db_crud.get_all_members()
        
        # Update proposal to debating status
        await db_crud.update_proposal_status(proposal_id, ProposalStatus.DEBATING)
        
        # Create a new debate
        debate = await db_crud.create_debate({
            "proposal_id": proposal_id,
            "title": f"Debate on {proposal.title}"
        })
        
        # Simulate debate
        debate_entries = await self.simulate_debate(proposal, members, debate.id, db_crud)
        
        # Generate debate summary
        debate_summary = await self.agent.generate_debate_summary(debate_entries)
        
        # Update proposal to voting status
        await db_crud.update_proposal_status(proposal_id, ProposalStatus.VOTING)
        
        # Simulate voting
        votes = await self.simulate_voting(proposal_id, proposal, members, debate_summary, db_crud)
        
        return {
            "proposal": proposal,
            "debate": debate,
            "debate_entries": debate_entries,
            "votes": votes
        }
