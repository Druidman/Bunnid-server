import sqlite3
from ..utils import DbResult, dbFunction

@dbFunction
def check_if_token_in_db(token: str, db: sqlite3.Cursor) -> DbResult:
    
    db.execute("SELECT id FROM UserSessions WHERE token=:token LIMIT 1",{"token": token})
    if (db.fetchone()):
        return DbResult(True, True)
    else:
        return DbResult(True, False) 
   
@dbFunction
def add_token_to_db(token: str, userId: int,  db: sqlite3.Cursor) -> DbResult:
    if (userId <= -1 or not token):
        return DbResult(False, "Wrong token or userId")
    
    db.execute("INSERT INTO UserSessions(token, userId) VALUES(:token, :userId)",{"token": token, "userId": userId})
    db.connection.commit()
    return DbResult(True, True)


@dbFunction
def get_token_data(token: str, db: sqlite3.Cursor) -> DbResult:
    if ( not token):
        return DbResult(False, "Wrong token")
    
    db.execute("SELECT userId, id FROM UserSessions WHERE token=:token LIMIT 1",{"token": token})
    row = db.fetchone()
    print(row)
    if not row:
        return DbResult(False, "")
    return DbResult(True, row)


    
    