from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.crud.party import get_parties

# Dynamic context generation based on database parties
def get_dutch_parliament_context(db: Session) -> str:
    """
    Generate context about the Dutch parliament with parties from the database
    """
    # Fetch parties from the database
    parties = get_parties(db)
    
    # Format party information
    party_lines = []
    for party in parties:
        party_lines.append(f"- {party.abbreviation}: {party.ideology}")
    
    party_info = "\n".join(party_lines) if party_lines else "Various political parties across the political spectrum."
    
    return f"""
You are simulating a member of the Dutch parliament (Tweede Kamer).

The Dutch parliament has multiple political parties:
{party_info}

The Dutch parliament typically debates and votes on legislative proposals.
"""

def get_debate_prompt(db: Session, member_data: Dict[Any, Any], proposal_data: Dict[Any, Any]) -> str:
    """
    Generate a prompt for a parliament member to debate a law proposal
    """
    context = get_dutch_parliament_context(db)
    
    return f"""
{context}

You are {member_data['name']}, a member of the {member_data['party']['name']} ({member_data['party']['abbreviation']}).
Your role is: {member_data['role']}

Professional background: 
- Career: {member_data.get('career', 'Not specified')}
- Other positions: {member_data.get('career2', 'Not specified')}
- Education: {member_data.get('education', 'Not specified')}

You are participating in a debate about the following proposal:

Title: {proposal_data['title']}
Content: {proposal_data['content']}
Proposed by: {proposal_data['proposer']['name']} ({proposal_data['proposer']['party']['abbreviation']})

Generate a realistic 2-3 paragraph statement or question that you would make during this debate. 
Ensure it reflects your party's ideology and your professional background. Use a formal but engaging parliamentary speaking style.
Be specific in your points, addressing particular aspects of the proposal, rather than making general comments.
"""

def get_voting_prompt(db: Session, member_data: Dict[Any, Any], proposal_data: Dict[Any, Any], debate_summary: str) -> str:
    """
    Generate a prompt for a parliament member to vote on a law proposal
    """
    context = get_dutch_parliament_context(db)
    
    return f"""
{context}

You are {member_data['name']}, a member of the {member_data['party']['name']} ({member_data['party']['abbreviation']}).
Your role is: {member_data['role']}

Professional background: 
- Career: {member_data.get('career', 'Not specified')}
- Other positions: {member_data.get('career2', 'Not specified')}
- Education: {member_data.get('education', 'Not specified')}

You need to vote on the following proposal:

Title: {proposal_data['title']}
Content: {proposal_data['content']}
Proposed by: {proposal_data['proposer']['name']} ({proposal_data['proposer']['party']['abbreviation']})

Summary of the debate: {debate_summary}

Based on your party's ideology and your professional background, how would you vote on this proposal?

Reply with ONLY ONE of the following options:
- FOR (if you support the proposal)
- AGAINST (if you oppose the proposal)
- ABSTAIN (if you choose to abstain from voting)
"""

def get_debate_summary_prompt(db: Session, debate_entries: List[Dict[Any, Any]]) -> str:
    """
    Generate a prompt to summarize a debate
    """
    context = get_dutch_parliament_context(db)
    
    debate_text = "\n\n".join([
        f"{entry['member']['name']} ({entry['member']['party']['abbreviation']}): {entry['content']}"
        for entry in debate_entries
    ])
    
    return f"""
{context}

Below is a transcript of a debate in the Dutch parliament:

{debate_text}

Provide a neutral, factual summary of this debate in 3-4 paragraphs. Include:
1. The main points raised by different parties
2. Key areas of agreement and disagreement
3. The general tone of the debate

Do not add your own opinions or perspectives. Stick strictly to summarizing what was said.
"""