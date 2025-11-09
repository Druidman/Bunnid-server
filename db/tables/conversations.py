import sqlite3
from ..utils import DB_RESULT, dbFunction

@dbFunction
def get_conversation(convId: int, db: sqlite3.Cursor) -> dict:
    if (convId <= -1):
        return DB_RESULT(False, "wrong convId")
    
    db.execute("SELECT title, id FROM conversations WHERE conversationId=:convId LIMIT 1", {
        "convId": convId
    })
    rows = db.fetchone()
    if (not rows):
        return DB_RESULT(False, "No such conversation")
    return DB_RESULT(True, rows)

@dbFunction
def get_conversations(limit: int, db: sqlite3.Cursor) -> dict:
    if (limit <= 0):
        return DB_RESULT(False, "wrong limit")
    
    db.execute("SELECT title, id FROM conversations WHERE LIMIT :limit", {
        "limit": limit
    })
    rows = db.fetchall()
    if (not rows):
        return DB_RESULT(False, "No conversations")
    return DB_RESULT(True, rows)


@dbFunction
def get_conversation_by_title(title: str, db: sqlite3.Cursor) -> dict:
    if (title == ""):
        return DB_RESULT(False, "wrong conv ntitleame")
    
    db.execute("SELECT conversationId FROM conversations WHERE title=:title", {
        "title": title
    })
    rows = db.fetchone()
    return DB_RESULT(True, rows)


@dbFunction
def add_conversation(title: str, db: sqlite3.Cursor) -> dict:
    if (title==""):
        return DB_RESULT(False, "wrong title")
    
    db.execute("INSERT INTO conversations(title) VALUES(:title)", {
        "title": title
    })
    db.connection.commit()
    return DB_RESULT(True, True)