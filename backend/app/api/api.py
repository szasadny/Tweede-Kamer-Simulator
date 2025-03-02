from fastapi import APIRouter

from app.api.endpoints import members, parties, proposals, debates, votes, simulation

api_router = APIRouter()
api_router.include_router(members.router, prefix="/members", tags=["members"])
api_router.include_router(parties.router, prefix="/parties", tags=["parties"])
api_router.include_router(proposals.router, prefix="/proposals", tags=["proposals"])
api_router.include_router(debates.router, prefix="/debates", tags=["debates"])
api_router.include_router(votes.router, prefix="/votes", tags=["votes"])
api_router.include_router(simulation.router, prefix="/simulation", tags=["simulation"])
