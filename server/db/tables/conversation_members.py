import sqlite3
from ..utils import DbResult, dbFunction

@dbFunction
def get_members(convId: int, db: sqlite3.Cursor) -> DbResult:
    if (convId <= -1):
        return DbResult(False, "wrong convId")
    
    db.execute("SELECT userId FROM conversation_members WHERE conversationId=:convId", {
        "convId": convId
    })
    rows = db.fetchall()
    return DbResult(True, rows, True)


@dbFunction
def add_member(convId: int,userId: int, db: sqlite3.Cursor) -> DbResult:
    if (convId <= -1 or userId <= -1):
        return DbResult(False, "wrong convId or userId")
    
    db.execute("INSERT INTO conversation_members(conversationId, userId) VALUES(:convId, :userId)", {
        "convId": convId,
        "userId": userId,
    })
    db.connection.commit()
    return DbResult(True, True)