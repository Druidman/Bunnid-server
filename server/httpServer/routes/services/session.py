
from fastapi import APIRouter
from server.httpServer.session.rt_session import make_RTS

import server.globals as globals



session_router = APIRouter(prefix="/session")

@session_router.get("/")
async def main_route() -> str:
    return "<h1>RT Session Bunnid api</h1>"

@session_router.get("/getRTS")
async def get_realtime_session() -> globals.APIResponse:
    rts_token: str = await make_RTS()
    if (not rts_token):
        return globals.errors["FAILED_TO_ASSIGN_TOKEN"]
    
    return globals.API_RESPONSE(True, {"token":rts_token})



