from fastapi import APIRouter
from .databaseService import users

database_router = APIRouter(prefix="/database")

database_router.include_router(users)


@database_router.get("/")
def databaseMain() -> str:
    return "<h1>This is database api!</h1>"
