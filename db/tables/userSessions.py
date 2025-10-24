import sqlite3
from ..utils import DB_RESULT


def check_if_token_in_db(token: str, db: sqlite3.Cursor) -> dict:
    try:
        db.execute("SELECT id FROM UserSessions WHERE token=:token LIMIT 1",{"token": token})
        if (db.fetchone()):
            return DB_RESULT(True, True)
        else:
            return DB_RESULT(True, False) 
    except sqlite3.Error as e:
        return DB_RESULT(False, e)


    
    