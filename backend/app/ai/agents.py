from typing import Dict, Any, List
import random
from app.models.vote import VoteType
from app.ai.client import MistralClient
from app.ai.prompts import get_debate_prompt, get_voting_prompt, get_debate_summary_prompt

class ParliamentaryAgent:
    def __init__(self, client: MistralClient = None):
        self.client = client or MistralClient()

    async def generate_debate_entry(self, member_data: Dict[Any, Any], proposal_data: Dict[Any, Any]) -> str:
        """
        Generate a debate entry for a parliament member
        """
        prompt = get_debate_prompt(member_data, proposal_data)
        response = await self.client.generate_response(prompt, temperature=0.8)
        return response

    async def generate_vote(self, member_data: Dict[Any, Any], proposal_data: Dict[Any, Any], debate_summary: str) -> VoteType:
        """
        Generate a vote for a parliament member
        """
        prompt = get_voting_prompt(member_data, proposal_data, debate_summary)
        response = await self.client.generate_response(prompt, temperature=0.5)

        # Parse the response to get the vote
        response_clean = response.strip().upper()

        if "FOR" in response_clean:
            return VoteType.FOR
        elif "AGAINST" in response_clean:
            return VoteType.AGAINST
        elif "ABSTAIN" in response_clean:
            return VoteType.ABSTAIN
        else:
            # Default to a random vote if the response is unclear
            return random.choice([VoteType.FOR, VoteType.AGAINST, VoteType.ABSTAIN])

    async def generate_debate_summary(self, debate_entries: List[Dict[Any, Any]]) -> str:
        """
        Generate a summary of a debate
        """
        prompt = get_debate_summary_prompt(debate_entries)
        response = await self.client.generate_response(prompt, temperature=0.5, max_tokens=1000)
        return response
