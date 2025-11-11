import sqlite3
from ..utils import DbResult, dbFunction

@dbFunction
def get_conversation(convId: int, db: sqlite3.Cursor) -> DbResult:
    if (convId <= -1):
        return DbResult(False, "wrong convId")
    
    db.execute("SELECT title, id FROM conversations WHERE conversationId=:convId LIMIT 1", {
        "convId": convId
    })
    rows = db.fetchone()
    if (not rows):
        return DbResult(False, "No such conversation")
    return DbResult(True, rows, True)

@dbFunction
def get_conversations(limit: int, db: sqlite3.Cursor) -> DbResult:
    if (limit <= 0):
        return DbResult(False, "wrong limit")
    
    db.execute("SELECT title, id FROM conversations LIMIT :limit", {
        "limit": limit
    })
    rows = db.fetchall()
    if (not rows):
        return DbResult(False, "No conversations")
    return DbResult(True, rows, True)


@dbFunction
def get_conversation_by_title(title: str, db: sqlite3.Cursor) -> DbResult:
    if (title == ""):
        return DbResult(False, "wrong conv title")
    
    db.execute("SELECT conversationId FROM conversations WHERE title=:title", {
        "title": title
    })
    rows = db.fetchone()
    return DbResult(True, rows, True)


@dbFunction
def add_conversation(title: str, db: sqlite3.Cursor) -> DbResult:
    if (title==""):
        return DbResult(False, "wrong title")
    
    db.execute("INSERT INTO conversations(title) VALUES(:title)", {
        "title": title
    })
    db.connection.commit()
    return DbResult(True, True)