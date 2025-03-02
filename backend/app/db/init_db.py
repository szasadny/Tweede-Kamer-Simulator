import asyncio
import json
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.database import engine, Base
from app.models.party import Party
from app.models.member import Member
from app.models.proposal import Proposal, ProposalStatus

# Sample Dutch parties data
PARTIES_DATA = [
    {
        "name": "Volkspartij voor Vrijheid en Democratie",
        "abbreviation": "VVD",
        "ideology": "Liberal-Conservative",
        "description": "Center-right political party focused on economic liberalism, conservative social values, and individual responsibility."
    },
    {
        "name": "Democraten 66",
        "abbreviation": "D66",
        "ideology": "Social Liberal",
        "description": "Progressive, social-liberal party focused on direct democracy, social and governmental reform, and environmental issues."
    },
    {
        "name": "Partij voor de Vrijheid",
        "abbreviation": "PVV",
        "ideology": "Right-wing Populist",
        "description": "Right-wing populist party with an anti-immigration, anti-Islam, Eurosceptic, and economically mixed platform."
    },
    {
        "name": "Christen-Democratisch Appèl",
        "abbreviation": "CDA",
        "ideology": "Christian Democratic",
        "description": "Christian democratic party with center-right positions and focus on traditional values."
    },
    {
        "name": "Socialistische Partij",
        "abbreviation": "SP",
        "ideology": "Socialist",
        "description": "Left-wing socialist party focused on workers' rights, welfare state, and opposition to neoliberalism."
    },
    {
        "name": "Partij van de Arbeid",
        "abbreviation": "PvdA",
        "ideology": "Social Democratic",
        "description": "Center-left social democratic party with focus on labor rights, social welfare, and progressive taxation."
    },
    {
        "name": "GroenLinks",
        "abbreviation": "GL",
        "ideology": "Green Politics",
        "description": "Left-wing green party focusing on environmentalism, social justice, and progressive politics."
    }
]

# Sample members data (with political leanings)
MEMBERS_DATA = [
    {
        "name": "Mark Rutte",
        "party_abbreviation": "VVD",
        "role": "MP",
        "economic_leaning": 75.0,
        "social_leaning": 55.0,
        "eu_stance": 40.0,
        "bio": "Former Prime Minister and VVD party leader with a focus on economic growth and fiscal responsibility."
    },
    {
        "name": "Sophie Hermans",
        "party_abbreviation": "VVD",
        "role": "MP",
        "economic_leaning": 70.0,
        "social_leaning": 50.0,
        "eu_stance": 45.0,
        "bio": "Fiscal conservative with expertise in budget affairs and economic policy."
    },
    {
        "name": "Sigrid Kaag",
        "party_abbreviation": "D66",
        "role": "MP",
        "economic_leaning": 55.0,
        "social_leaning": 25.0,
        "eu_stance": 20.0,
        "bio": "Progressive politician with a background in international diplomacy and strong pro-EU stance."
    },
    {
        "name": "Rob Jetten",
        "party_abbreviation": "D66",
        "role": "MP",
        "economic_leaning": 50.0,
        "social_leaning": 20.0,
        "eu_stance": 15.0,
        "bio": "Young, progressive politician with focus on climate action and democratic reform."
    },
    {
        "name": "Geert Wilders",
        "party_abbreviation": "PVV",
        "role": "MP",
        "economic_leaning": 65.0,
        "social_leaning": 85.0,
        "eu_stance": 90.0,
        "bio": "Outspoken critic of Islam and immigration, with strong nationalist and Eurosceptic views."
    },
    {
        "name": "Fleur Agema",
        "party_abbreviation": "PVV",
        "role": "MP",
        "economic_leaning": 60.0,
        "social_leaning": 80.0,
        "eu_stance": 85.0,
        "bio": "Focused on healthcare issues while maintaining strong anti-immigration stance."
    },
    {
        "name": "Wopke Hoekstra",
        "party_abbreviation": "CDA",
        "role": "MP",
        "economic_leaning": 65.0,
        "social_leaning": 60.0,
        "eu_stance": 40.0,
        "bio": "Former finance minister with expertise in economic policy and moderate conservative values."
    },
    {
        "name": "Lilian Marijnissen",
        "party_abbreviation": "SP",
        "role": "MP",
        "economic_leaning": 20.0,
        "social_leaning": 30.0,
        "eu_stance": 60.0,
        "bio": "Strong advocate for workers' rights, social equality, and critical of EU neoliberal policies."
    },
    {
        "name": "Attje Kuiken",
        "party_abbreviation": "PvdA",
        "role": "MP",
        "economic_leaning": 35.0,
        "social_leaning": 30.0,
        "eu_stance": 30.0,
        "bio": "Social democrat with focus on healthcare, education, and labor market issues."
    },
    {
        "name": "Jesse Klaver",
        "party_abbreviation": "GL",
        "role": "MP",
        "economic_leaning": 25.0,
        "social_leaning": 15.0,
        "eu_stance": 25.0,
        "bio": "Young, charismatic leader with strong focus on climate action, social justice, and progressive taxation."
    }
]

# Sample proposals
PROPOSALS_DATA = [
    {
        "title": "Climate Adaptation Act",
        "content": "A proposal to allocate 10 billion euros over the next 5 years for climate adaptation projects, focusing on flood protection, drought management, and sustainable agriculture. The act aims to prepare the Netherlands for the impacts of climate change by investing in infrastructure, research, and community resilience programs.",
        "proposer_name": "Jesse Klaver",
        "status": "draft"
    },
    {
        "title": "Digital Privacy Protection Framework",
        "content": "This proposal establishes a comprehensive framework for protecting citizens' digital privacy rights. It includes stricter regulations for data collection by both government and private entities, enhanced transparency requirements, stronger consent mechanisms, and higher penalties for data breaches. The framework also establishes an independent oversight body to monitor compliance and investigate complaints.",
        "proposer_name": "Rob Jetten",
        "status": "draft"
    },
    {
        "title": "Immigration Reform Act",
        "content": "A proposal to reform the immigration system with stricter entry requirements, more efficient processing of asylum applications, and enhanced border security measures. The act also includes provisions for integration programs for accepted refugees and a points-based system for economic migrants based on skills, education, and language proficiency.",
        "proposer_name": "Geert Wilders",
        "status": "draft"
    }
]

async def init_db():
    """Initialize the database with sample data."""
    Base.metadata.create_all(bind=engine)
    
    party_abbreviation_to_id = {}
    member_name_to_id = {}
    
    with Session(engine) as db:
        # Add parties
        for party_data in PARTIES_DATA:
            db_party = Party(**party_data)
            db.add(db_party)
            db.flush()
            party_abbreviation_to_id[party_data["abbreviation"]] = db_party.id
        
        db.commit()
        
        # Add members
        for member_data in MEMBERS_DATA:
            party_abbreviation = member_data.pop("party_abbreviation")
            party_id = party_abbreviation_to_id.get(party_abbreviation)
            if not party_id:
                print(f"Party with abbreviation {party_abbreviation} not found")
                continue
                
            db_member = Member(
                party_id=party_id,
                **{k: v for k, v in member_data.items()}
            )
            db.add(db_member)
            db.flush()
            member_name_to_id[member_data["name"]] = db_member.id
        
        db.commit()
        
        # Add proposals
        for proposal_data in PROPOSALS_DATA:
            proposer_name = proposal_data.pop("proposer_name")
            status = proposal_data.pop("status")
            proposer_id = member_name_to_id.get(proposer_name)
            if not proposer_id:
                print(f"Member with name {proposer_name} not found")
                continue
                
            db_proposal = Proposal(
                proposer_id=proposer_id,
                status=status,
                **proposal_data
            )
            db.add(db_proposal)
        
        db.commit()
    
    print("Database initialized with sample data!")

if __name__ == "__main__":
    asyncio.run(init_db())
