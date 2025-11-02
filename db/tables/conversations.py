import sqlite3
from ..utils import DB_RESULT, dbFunction

@dbFunction
def get_conversation(convId: int, db: sqlite3.Cursor) -> dict:
    if (convId <= -1):
        return DB_RESULT(False, "wrong convId")
    
    db.execute("SELECT title FROM conversations WHERE conversationId=:convId", {
        "convId": convId
    })
    rows = db.fetchone()
    return DB_RESULT(True, rows)

@dbFunction
def get_conversation_by_name(name: str, db: sqlite3.Cursor) -> dict:
    if (name == ""):
        return DB_RESULT(False, "wrong conv name")
    
    db.execute("SELECT conversationId FROM conversations WHERE name=:name", {
        "name": name
    })
    rows = db.fetchone()
    return DB_RESULT(True, rows)


@dbFunction
def add_conversation(name: str, db: sqlite3.Cursor) -> dict:
    if (name==""):
        return DB_RESULT(False, "wrong name")
    
    db.execute("INSERT INTO conversations(name) VALUES(:name)", {
        "name": name
    })
    db.connection.commit()
    return DB_RESULT(True, True)