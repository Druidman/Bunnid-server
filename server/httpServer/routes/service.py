from fastapi import APIRouter, Depends
from .services import conversation_router
from .services import database_router
from server.httpServer.auth.session_token import verify_session_token_header

service_router = APIRouter(prefix="/service", dependencies=[Depends(verify_session_token_header)])

service_router.include_router(conversation_router)
service_router.include_router(database_router)



@service_router.get("/")
def serviceMain() -> str:
    return "<h1>This is service api! /conversation, /database</h1>"


