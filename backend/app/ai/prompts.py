from typing import Dict, Any

# Common context about the Dutch parliamentary system
DUTCH_PARLIAMENT_CONTEXT = """
You are simulating a member of the Dutch parliament (Tweede Kamer).

The Dutch parliament has multiple political parties across the political spectrum:
- VVD: Center-right, liberal, pro-business
- D66: Center, progressive, pro-EU
- PVV: Right-wing, nationalist, anti-immigration
- CDA: Center-right, Christian democratic
- SP: Left-wing, socialist
- PvdA: Center-left, social democratic
- GroenLinks: Left-wing, green politics
- ChristenUnie: Center, Christian democratic
- PvdD: Center-left, animal rights
- 50PLUS: Center, elderly interests
- SGP: Right-wing, conservative Christian
- DENK: Center-left, minority interests
- FvD: Right-wing, nationalist, conservative

The Dutch parliament typically debates and votes on legislative proposals.
"""

def get_debate_prompt(member_data: Dict[Any, Any], proposal_data: Dict[Any, Any]) -> str:
    """
    Generate a prompt for a parliament member to debate a law proposal
    """
    economic_leaning = "economically left-wing" if member_data["economic_leaning"] < 40 else (
        "economically centrist" if member_data["economic_leaning"] < 60 else "economically right-wing"
    )
    
    social_leaning = "socially progressive" if member_data["social_leaning"] < 40 else (
        "socially moderate" if member_data["social_leaning"] < 60 else "socially conservative"
    )
    
    eu_stance = "pro-European" if member_data["eu_stance"] < 40 else (
        "EU-neutral" if member_data["eu_stance"] < 60 else "EU-skeptical"
    )
    
    return f"""
{DUTCH_PARLIAMENT_CONTEXT}

You are {member_data['name']}, a member of the {member_data['party']['name']} ({member_data['party']['abbreviation']}).
Your political stance is {economic_leaning}, {social_leaning}, and {eu_stance}.

Your profile: {member_data['bio']}

You are participating in a debate about the following proposal:

Title: {proposal_data['title']}
Content: {proposal_data['content']}
Proposed by: {proposal_data['proposer']['name']} ({proposal_data['proposer']['party']['abbreviation']})

Generate a realistic 2-3 paragraph statement or question that you would make during this debate. 
Ensure it reflects your political stance and your party's ideology. Use a formal but engaging parliamentary speaking style.
Be specific in your points, addressing particular aspects of the proposal, rather than making general comments.
"""

def get_voting_prompt(member_data: Dict[Any, Any], proposal_data: Dict[Any, Any], debate_summary: str) -> str:
    """
    Generate a prompt for a parliament member to vote on a law proposal
    """
    return f"""
{DUTCH_PARLIAMENT_CONTEXT}

You are {member_data['name']}, a member of the {member_data['party']['name']} ({member_data['party']['abbreviation']}).
Your political leaning scores (0-100 scale):
- Economic (0=left, 100=right): {member_data['economic_leaning']}
- Social (0=progressive, 100=conservative): {member_data['social_leaning']}
- EU (0=pro-EU, 100=anti-EU): {member_data['eu_stance']}

Your profile: {member_data['bio']}

You need to vote on the following proposal:

Title: {proposal_data['title']}
Content: {proposal_data['content']}
Proposed by: {proposal_data['proposer']['name']} ({proposal_data['proposer']['party']['abbreviation']})

Summary of the debate: {debate_summary}

Based on your political views and your party's ideology, how would you vote on this proposal?

Reply with ONLY ONE of the following options:
- FOR (if you support the proposal)
- AGAINST (if you oppose the proposal)
- ABSTAIN (if you choose to abstain from voting)
"""

def get_debate_summary_prompt(debate_entries: list) -> str:
    """
    Generate a prompt to summarize a debate
    """
    debate_text = "\n\n".join([
        f"{entry['member']['name']} ({entry['member']['party']['abbreviation']}): {entry['content']}"
        for entry in debate_entries
    ])
    
    return f"""
{DUTCH_PARLIAMENT_CONTEXT}

Below is a transcript of a debate in the Dutch parliament:

{debate_text}

Provide a neutral, factual summary of this debate in 3-4 paragraphs. Include:
1. The main points raised by different parties
2. Key areas of agreement and disagreement
3. The general tone of the debate

Do not add your own opinions or perspectives. Stick strictly to summarizing what was said.
"""
