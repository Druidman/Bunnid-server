from fastapi import APIRouter

import server.globals as globals
from server.httpServer.auth.user_session import userSession
from server.db.tables.users import get_users_preview

users_router = APIRouter(prefix="/users")

@users_router.route("/", methods=["GET"])
def usersMain() -> str:
    return "<h1>This is database/users api! (/get)</h1>"


@users_router.route("/get", methods=["GET"])
@userSession
async def usersGet() -> globals.APIResponse:
    result = await get_users_preview(100,db=globals.connPool)
    return globals.api_response_from_db_response(result)
    