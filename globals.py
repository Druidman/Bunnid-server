
import sqlite3

def api_response_from_db_repsonse(result: dict) -> dict:
    if (not result["STATUS"]):
        return API_RESPONSE(False, result["msg"])
    return API_RESPONSE(True, result["msg"])

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


