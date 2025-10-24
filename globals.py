
import sqlite3

API_RESPONSE = lambda stat, msg: {
    "STATUS": stat,
    "MSG": msg
}
USER_TOKEN_LENGTH: int = 15
dbConn: sqlite3.Connection | None = None

errors = {

    "NO_JSON": API_RESPONSE(False, "No json found in request"),
    "ACCES_DENIED": API_RESPONSE(False, "Acces denied"),
    "NO_ARGS": API_RESPONSE(False, "No args found in request")
}
