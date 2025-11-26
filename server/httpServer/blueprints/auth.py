from fastapi import APIRouter
from pydantic import BaseModel
from server.db.tables.users import check_if_user_exists, add_new_user, get_user_by_login
from server.db.tables.userSessions import get_token_data
from ..auth import make_user_session

from server import globals
from server.db.utils import DbResult

auth = APIRouter(prefix="/auth")

@auth.route("/")
def testRoute():
    return "<h1>Auth Bunnid API</h1>"

class LoginData(BaseModel):
    login: str
    password: str

@auth.post("/login")
async def login(data: LoginData):
    res: DbResult = check_if_user_exists( data.login, data.password, globals.dbConn.cursor())
    if (not res.status):
        return globals.errors["LOGIN_TRY_AGAIN"]
    else:
        if (not res.msg):
            return globals.errors["INCORRECT_LOGIN_VALUES"]
        
        userRes = get_user_by_login(data.login, globals.dbConn.cursor())
        if (not userRes.status):
            return globals.errors["LOGIN_TRY_AGAIN"]
      
        userId = userRes.msg["id"]
        

        token = make_user_session(userId)
        if not token:

            return globals.errors["FAILED_TO_ASSIGN_TOKEN"]
        else:
            return globals.API_RESPONSE(True, {
                "token": token, 
                "userId": userId
            })


@auth_bp.route("/register", methods=["POST"])
def register():
    name: str | None = request.json.get("name")
    login: str | None = request.json.get("login")
    password: str | None = request.json.get("password")
    if (not name or not login or not password):
        return globals.API_RESPONSE(False, "Password, name, login not provided")
    
    res = add_new_user(name, login, password, globals.dbConn.cursor())
    
    return globals.API_RESPONSE(res.status, res.msg)


