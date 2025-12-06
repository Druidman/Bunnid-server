from fastapi import APIRouter, Depends
from .services import conversation_router
from .services import database_router
from .services import session_router
from server.httpServer.auth.user_session import verify_user_session_jwt

service_router = APIRouter(prefix="/service", dependencies=[Depends(verify_user_session_jwt)])

service_router.include_router(conversation_router)
service_router.include_router(database_router)
service_router.include_router(session_router)



@service_router.get("/")
def serviceMain() -> str:
    return "<h1>This is service api! /conversation, /database</h1>"


