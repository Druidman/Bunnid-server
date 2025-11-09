import sqlite3
from ..utils import DB_RESULT, dbFunction

@dbFunction
def check_if_token_in_db(token: str, db: sqlite3.Cursor) -> dict:
    
    db.execute("SELECT id FROM UserSessions WHERE token=:token LIMIT 1",{"token": token})
    if (db.fetchone()):
        return DB_RESULT(True, True)
    else:
        return DB_RESULT(True, False) 
   
@dbFunction
def add_token_to_db(token: str, userId: int,  db: sqlite3.Cursor) -> dict:
    if (userId <= -1 or not token):
        return DB_RESULT(False, "Wrong token or userId")
    
    db.execute("INSERT INTO UserSessions(token, userId) VALUES(:token, :userId)",{"token": token, "userId": userId})
    db.connection.commit()
    return DB_RESULT(True, True)


@dbFunction
def get_token_data(token: str, db: sqlite3.Cursor) -> dict:
    if ( not token):
        return DB_RESULT(False, "Wrong token")
    
    db.execute("SELECT userId, id FROM UserSessions WHERE token=:token LIMIT 1",{"token": token})
    row = db.fetchone()
    print(row)
    if not row:
        return DB_RESULT(False, "")
    return DB_RESULT(True, row)


    
    