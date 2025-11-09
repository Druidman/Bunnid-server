
import sqlite3
from server.db.utils import DbResult

def api_response_from_db_repsonse(result: DbResult) -> dict:
    if result.makeMsgDict():
        return API_RESPONSE(result.status, result.msgDict)
    else:
        return API_RESPONSE(result.status, result.msg)
    

API_RESPONSE = lambda stat, msg: {
    "STATUS": stat,
    "MSG": msg
}


USER_TOKEN_LENGTH: int = 15
RTS_TOKEN_LENGTH: int = 15
dbConn: sqlite3.Connection | None = None

errors = {

    "NO_JSON": API_RESPONSE(False, "No json found in request"),
    "ACCES_DENIED": API_RESPONSE(False, "Acces denied"),
    "NO_ARGS": API_RESPONSE(False, "No args found in request"),
    "INCORRECT_LOGIN_VALUES": API_RESPONSE(False, "Incorrect login or password"),
    "LOGIN_TRY_AGAIN": API_RESPONSE(False, "Smth went wrong try loggin in again"),
    "FAILED_TO_ASSIGN_TOKEN": API_RESPONSE(False, "Failed to assign token to the user")
}


