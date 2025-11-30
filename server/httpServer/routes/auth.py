from typing import Optional
import asyncpg
from fastapi import APIRouter, Body
from server.db.tables.users import add_new_user, get_full_user
from ..auth import make_user_session
from pydantic import BaseModel

import server.globals as globals
from server.db.utils import DbResult

auth_router = APIRouter(prefix="/auth")

@auth_router.get("/")
async def testRoute() -> str:
    return "<h1>Auth Bunnid API</h1>"

class LoginResponse(BaseModel):
    token: str
    user_id: int

@auth_router.post("/login")
async def login(
    login: str = Body(..., min_length=1),
    password: str = Body(..., min_length=1)
) -> globals.APIResponse[LoginResponse]:
    
    res: DbResult[Optional[asyncpg.Record]] = await get_full_user(login, password, globals.connPool) 
    if (res.error):
        return globals.API_RESPONSE(error=res.error, response=None)
    
    token = await make_user_session(user_id=res.result.get("id"))
    if not token:
        return globals.errors["FAILED_TO_ASSIGN_TOKEN"]
    else:
        return globals.API_RESPONSE(response = {
            "token": token, 
            "user_id": res.result.get("id")
        })

class RegisterResponse(BaseModel):
    result: bool | None

@auth_router.post("/register")
async def register(
    login: str = Body(..., min_length=1),
    password: str = Body(..., min_length=1),
    name: str = Body(..., min_length=1)
) -> globals.APIResponse[RegisterResponse]:
    if (not name or not login or not password):
        return globals.API_RESPONSE[None](error="Password, name, login not provided")
    
    res: DbResult[Optional[bool]] = await add_new_user(name, login, password, globals.connPool)
    
    return globals.API_RESPONSE(error=res.error, response={"result": res.result})


