import sqlite3
from ..utils import DB_RESULT, dbFunction

@dbFunction
def get_members(convId: int, db: sqlite3.Cursor) -> dict:
    if (convId <= -1):
        return DB_RESULT(False, "wrong convId")
    
    db.execute("SELECT userId FROM conversation_members WHERE conversationId=:convId", {
        "convId": convId
    })
    rows = db.fetchall()
    return DB_RESULT(True, rows)


@dbFunction
def add_member(convId: int,userId: int, db: sqlite3.Cursor) -> dict:
    if (convId <= -1 or userId <= -1):
        return DB_RESULT(False, "wrong convId or userId")
    
    db.execute("INSERT INTO conversation_members(conversationId, userId) VALUES(:convId, :userId)", {
        "convId": convId,
        "userId": userId,
    })
    db.connection.commit()
    return DB_RESULT(True, True)