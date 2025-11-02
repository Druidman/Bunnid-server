import sqlite3
from ..utils import DB_RESULT, dbFunction

@dbFunction
def get_messages(convId: int, limit: int, db: sqlite3.Cursor) -> dict:
    if (limit < -1 or convId <= -1):
        return DB_RESULT(False, "wrong values for limit and convId")
    
    db.execute("SELECT userId, content FROM messages WHERE conversationId=:convId LIMIT :limit", {
        "convId": convId,
        "limit": limit
    })
    rows = db.fetchall()
    return DB_RESULT(True, rows)


@dbFunction
def add_message(convId: int, userId: int, content: str, db: sqlite3.Cursor) -> dict:
    if (userId <= -1 or convId <= -1 or content==""):
        return DB_RESULT(False, "wrong values for userId or content or convId")
    
    db.execute("INSERT INTO messages(conversationId, userId, content) VALUES(:convId, :userId, :content)", {
        "convId": convId,
        "userId": userId,
        "content": content
    })
    db.connection.commit()
    return DB_RESULT(True, True)