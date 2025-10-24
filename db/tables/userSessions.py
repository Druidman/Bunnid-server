import sqlite3
from ..utils import DB_RESULT, dbFunction

@dbFunction
def check_if_token_in_db(token: str, db: sqlite3.Cursor) -> dict:
    
    db.execute("SELECT id FROM UserSessions WHERE token=:token LIMIT 1",{"token": token})
    if (db.fetchone()):
        return DB_RESULT(True, True)
    else:
        return DB_RESULT(True, False) 
   


    
    