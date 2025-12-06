from typing import Optional
import asyncpg
from fastapi import APIRouter, Body, Response, HTTPException
from server.db.tables.users import add_new_user, get_full_user
from pydantic import BaseModel
from server.httpServer.auth import create_session_refresh_token
import server.globals as globals
from server.db.utils import DbResult
import urllib.parse

auth_router = APIRouter(prefix="/auth")

@auth_router.get("/")
async def testRoute() -> str:
    return "<h1>Auth Bunnid API</h1>"

class LoginResponse(BaseModel):
    user_id: int

@auth_router.post("/login")
async def login(
    response: Response,
    login: str = Body(..., min_length=1),
    password: str = Body(..., min_length=1)
    
) -> globals.APIResponse[LoginResponse]:
    
    res: DbResult[Optional[asyncpg.Record]] = await get_full_user(login, password, globals.connPool) 
    if (res.error):
        return globals.API_RESPONSE(error=res.error, response=None)
    
    user_id = res.result.get("id")
    
    # now we have verified that request is comming from client who knows auth reqired info
    # This means that we need to generate some way to authenticate client without password and login later on

    # For that we:

    # Create jwt refresh token
    session_refresh_token: str = await create_session_refresh_token(user_id)
    if not session_refresh_token:
        raise HTTPException(status_code=500, detail="session refresh token not properly created")
    
    # sending token in cookie
    response.set_cookie(
        key="session-refresh-token",
        value=session_refresh_token,
        httponly=True, # protects against xss token steal
        samesite="strict", # protects against csrf attack
        secure=globals.PRODUCTION, # http/https
    )

    return globals.API_RESPONSE(response={
        "user_id": user_id
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


