from typing import TypedDict
from fastapi import APIRouter
from pydantic import BaseModel

import server.globals as globals
from server.db.tables.users import get_users_preview

users_router = APIRouter(prefix="/users")

@users_router.get("/")
def usersMain() -> str:
    return "<h1>This is database/users api! (/get)</h1>"


class UserPreviewModel(TypedDict):
    id: int
    name: str
class UsersGetResponse(BaseModel):
    users: list[UserPreviewModel]
@users_router.get("/get")
async def usersGet() -> globals.APIResponse[UsersGetResponse]:
    result = await get_users_preview(100,db=globals.connPool)
    return globals.api_response_from_db_response(result)
    