# backend/app/db/init_db.py
import asyncio
import httpx
import logging
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.database import engine, Base
from app.models.party import Party
from app.models.member import Member
from app.models.proposal import Proposal, ProposalStatus

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API endpoints
TWEEDEKAMER_API_BASE = "https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0"
FRACTIES_ENDPOINT = f"{TWEEDEKAMER_API_BASE}/Fractie"
PERSONEN_ENDPOINT = f"{TWEEDEKAMER_API_BASE}/Persoon"
PERSOON_LOOPBAAN_ENDPOINT = f"{TWEEDEKAMER_API_BASE}/PersoonLoopbaan"
PERSOON_NEVENFUNCTIE_ENDPOINT = f"{TWEEDEKAMER_API_BASE}/PersoonNevenfunctie"
PERSOON_ONDERWIJS_ENDPOINT = f"{TWEEDEKAMER_API_BASE}/PersoonOnderwijs"

async def fetch_data(url, params=None):
    """Fetch data from the Tweede Kamer API"""
    if params is None:
        params = {}
    
    # Add standard parameters for JSON output and expanded entities
    params.update({
        "$format": "json",
        "$expand": "Fractie"  # Include related entities where appropriate
    })
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Error fetching data from {url}: {e}")
            return {"value": []}

async def fetch_all_fracties():
    """Fetch all political parties (fracties) from the API"""
    logger.info("Fetching political parties...")
    
    params = {
        "$filter": "Actief eq true",  # Only active parties
        "$select": "Id,Afkorting,NaamNL,DatumActief,DatumInactief"
    }
    
    response = await fetch_data(FRACTIES_ENDPOINT, params)
    return response.get("value", [])

async def fetch_all_personen():
    """Fetch all parliament members from the API"""
    logger.info("Fetching parliament members...")
    
    params = {
        "$filter": "Actief eq true",  # Only active members
        "$select": "Id,Roepnaam,Tussenvoegsel,Achternaam,Functie,FractieZetel/FractieId",
        "$expand": "FractieZetel"
    }
    
    response = await fetch_data(PERSONEN_ENDPOINT, params)
    return response.get("value", [])

async def fetch_person_details(person_id):
    """Fetch additional details for a specific person"""
    logger.info(f"Fetching details for person {person_id}...")
    
    # Fetch career information
    career_params = {
        "$filter": f"PersoonId eq {person_id}",
        "$select": "Id,PersoonId,Functie,Werkgever,Van,TotEnMet,Omschrijving"
    }
    career_response = await fetch_data(PERSOON_LOOPBAAN_ENDPOINT, career_params)
    
    # Fetch additional positions/functions
    nevenfunctie_params = {
        "$filter": f"PersoonId eq {person_id}",
        "$select": "Id,PersoonId,Functie,Werkgever,Van,TotEnMet,Omschrijving"
    }
    nevenfunctie_response = await fetch_data(PERSOON_NEVENFUNCTIE_ENDPOINT, nevenfunctie_params)
    
    # Fetch education information
    education_params = {
        "$filter": f"PersoonId eq {person_id}",
        "$select": "Id,PersoonId,Opleiding,Instelling,Van,TotEnMet,Omschrijving"
    }
    education_response = await fetch_data(PERSOON_ONDERWIJS_ENDPOINT, education_params)
    
    return {
        "career": career_response.get("value", []),
        "career2": nevenfunctie_response.get("value", []),
        "education": education_response.get("value", [])
    }

def format_career_text(career_items):
    """Format career items into readable text"""
    if not career_items:
        return None
    
    formatted_items = []
    for item in career_items:
        period = ""
        if item.get("Van"):
            period += f"From {item.get('Van')}"
        if item.get("TotEnMet"):
            period += f" to {item.get('TotEnMet')}"
        
        role = item.get("Functie", "")
        employer = item.get("Werkgever", "")
        description = item.get("Omschrijving", "")
        
        entry = f"{role} at {employer}" if employer else role
        if period:
            entry += f" ({period})"
        if description:
            entry += f": {description}"
            
        formatted_items.append(entry)
    
    return "\n".join(formatted_items)

def format_education_text(education_items):
    """Format education items into readable text"""
    if not education_items:
        return None
    
    formatted_items = []
    for item in education_items:
        period = ""
        if item.get("Van"):
            period += f"From {item.get('Van')}"
        if item.get("TotEnMet"):
            period += f" to {item.get('TotEnMet')}"
        
        education = item.get("Opleiding", "")
        institution = item.get("Instelling", "")
        description = item.get("Omschrijving", "")
        
        entry = f"{education} at {institution}" if institution else education
        if period:
            entry += f" ({period})"
        if description:
            entry += f": {description}"
            
        formatted_items.append(entry)
    
    return "\n".join(formatted_items)

async def init_db():
    """Initialize the database with data from the Tweede Kamer API"""
    Base.metadata.create_all(bind=engine)
    
    logger.info("Starting database initialization...")
    
    # Get data from API
    fracties = await fetch_all_fracties()
    personen = await fetch_all_personen()
    
    # Mapping of API IDs to database IDs
    fractie_id_map = {}
    
    with Session(engine) as db:
        # Add parties (fracties)
        logger.info(f"Adding {len(fracties)} political parties...")
        for fractie in fracties:
            db_party = Party(
                name=fractie.get("NaamNL", ""),
                abbreviation=fractie.get("Afkorting", ""),
                ideology="",  # API doesn't provide ideology information
                description=f"Active since {fractie.get('DatumActief', '')}"
            )
            db.add(db_party)
            db.flush()
            fractie_id_map[fractie.get("Id")] = db_party.id
        
        db.commit()
        
        # Add members (personen)
        logger.info(f"Adding {len(personen)} parliament members...")
        for person in personen:
            # Get person details
            person_id = person.get("Id")
            if not person_id:
                continue
                
            # Get the fractie (party) ID
            fractie_id = None
            fractie_zetel = person.get("FractieZetel", [])
            if isinstance(fractie_zetel, list) and fractie_zetel:
                fractie_id = fractie_zetel[0].get("FractieId")
            elif isinstance(fractie_zetel, dict):
                fractie_id = fractie_zetel.get("FractieId")
                
            if not fractie_id or fractie_id not in fractie_id_map:
                logger.warning(f"Skipping person {person_id}: No valid party ID")
                continue
                
            party_id = fractie_id_map[fractie_id]
            
            # Get additional details
            details = await fetch_person_details(person_id)
            
            # Format name
            roepnaam = person.get("Roepnaam", "")
            tussenvoegsel = person.get("Tussenvoegsel", "")
            achternaam = person.get("Achternaam", "")
            
            full_name = roepnaam
            if tussenvoegsel:
                full_name += f" {tussenvoegsel}"
            full_name += f" {achternaam}"
            
            # Format career, additional positions, and education information
            career_text = format_career_text(details.get("career", []))
            career2_text = format_career_text(details.get("career2", []))
            education_text = format_education_text(details.get("education", []))
            
            db_member = Member(
                name=full_name.strip(),
                party_id=party_id,
                role=person.get("Functie", "MP"),
                career=career_text,
                career2=career2_text,
                education=education_text
            )
            db.add(db_member)
        
        db.commit()
    
    logger.info("Database initialization completed successfully!")

if __name__ == "__main__":
    asyncio.run(init_db())