import secrets
from server.db.tables.userRTSessions import add_token_to_db
import server.globals as globals


def make_RTS() -> str:

    RTS_token = secrets.token_urlsafe(globals.RTS_TOKEN_LENGTH)
    result = add_token_to_db(token=RTS_token, db=globals.dbConn.cursor())
    if not result["STATUS"]:
        print(f"Error when adding RT token: {result['MSG']}")
        return ""
    else:
        return RTS_token
    