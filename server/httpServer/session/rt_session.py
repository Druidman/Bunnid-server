import secrets
from server.db.tables.user_rt_sessions import add_token_to_db
import server.globals as globals
from server.db.utils import DbResult


async def make_RTS() -> str:

    RTS_token = secrets.token_urlsafe(globals.RTS_TOKEN_LENGTH)
    result: DbResult = await add_token_to_db(token=RTS_token, connPool=globals.connPool)
    if not result.status:
        print(f"Error when adding RT token: {result.msg}")
        return ""
    else:
        return RTS_token
    