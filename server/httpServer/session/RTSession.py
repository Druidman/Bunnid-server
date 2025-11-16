import secrets
from server.db.tables.userRTSessions import add_token_to_db
import server.globals as globals
from server.db.utils import DbResult


def make_RTS() -> str:

    RTS_token = secrets.token_urlsafe(globals.RTS_TOKEN_LENGTH)
    result: DbResult = add_token_to_db(token=RTS_token, db=globals.dbConn.cursor())
    if not result.status:
        print(f"Error when adding RT token: {result.msg}")
        return ""
    else:
        return RTS_token
    