from fastapi import APIRouter
from .services import conversation
from .services import database

service_router = APIRouter(prefix="/service")

service_router.include_router(conversation)
service_router.include_router(database)


@service_router.get("/")
def serviceMain() -> str:
    return "<h1>This is service api! /conversation, /database</h1>"


