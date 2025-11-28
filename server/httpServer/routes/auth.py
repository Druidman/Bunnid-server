from fastapi import APIRouter, Body
from server.db.tables.users import check_if_user_exists, add_new_user, get_user_by_login, get_full_user
from ..auth import make_user_session

import server.globals as globals
from server.db.utils import DbResult

auth_router = APIRouter(prefix="/auth")

@auth_router.get("/")
async def testRoute() -> str:
    return "<h1>Auth Bunnid API</h1>"

@auth_router.post("/login")
async def login(
    login: str = Body(..., min_length=1),
    password: str = Body(..., min_length=1)
) -> globals.APIResponse:
    res: DbResult = await get_full_user(login, password, globals.connPool) 
    if (not res.status):
        return globals.errors["LOGIN_TRY_AGAIN"]
    
    if (not res.msg):
        return globals.errors["INCORRECT_LOGIN_VALUES"]
    
    if (not res.makeMsgDict()):
        return globals.errors["LOGIN_TRY_AGAIN"]
    

    token = await make_user_session(res.msgDict["id"])
    if not token:
        return globals.errors["FAILED_TO_ASSIGN_TOKEN"]
    else:
        return globals.API_RESPONSE(True, {
            "token": token, 
            "userId": res.msgDict["id"]
        })


@auth_router.post("/register")
async def register(
    login: str = Body(..., min_length=1),
    password: str = Body(..., min_length=1),
    name: str = Body(..., min_length=1)
) -> globals.APIResponse:
    if (not name or not login or not password):
        return globals.API_RESPONSE(False, "Password, name, login not provided")
    
    res: DbResult = await add_new_user(name, login, password, globals.connPool)
    
    return globals.API_RESPONSE(res.status, res.msg)


