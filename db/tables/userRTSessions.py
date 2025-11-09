import sqlite3
from ..utils import DbResult, dbFunction

@dbFunction
def check_if_token_in_db(token: str, db: sqlite3.Cursor) -> DbResult:
    
    db.execute("SELECT id FROM UserRTSessions WHERE token=:token LIMIT 1",{"token": token})
    if (db.fetchone()):
        return DbResult(True, True)
    else:
        return DbResult(True, False) 
   
@dbFunction
def add_token_to_db(token: str, db: sqlite3.Cursor) -> DbResult:
    db.execute("INSERT INTO UserRTSessions(token) VALUES(:token)",{"token": token})
    db.connection.commit()
    return DbResult(True, True)


    
    