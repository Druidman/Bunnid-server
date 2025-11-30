
from fastapi import APIRouter
from server.httpServer.session.rt_session import make_RTS

import server.globals as globals
from pydantic import BaseModel


session_router = APIRouter(prefix="/session")

@session_router.get("/")
async def main_route() -> str:
    return "<h1>RT Session Bunnid api</h1>"

class RtSessionResponse(BaseModel):
    token: str
@session_router.get("/getRTS")
async def get_realtime_session() -> globals.APIResponse[RtSessionResponse]:
    rts_token: str = await make_RTS()
    if (not rts_token):
        return globals.errors["FAILED_TO_ASSIGN_TOKEN"]
    
    return globals.API_RESPONSE(response={"token":rts_token})



