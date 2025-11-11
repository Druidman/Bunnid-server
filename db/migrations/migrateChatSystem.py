import sqlite3
from ..utils import DbResult, dbFunction

@dbFunction
def migrate_chat_system(db: sqlite3.Cursor) -> DbResult:
    
    db.execute("CREATE TABLE IF NOT EXISTS messages(" \
            "id INTEGER PRIMARY KEY AUTOINCREMENT," \
            "conversationId INTEGER," \
            "userId INTEGER," \
            "content TEXT" \
        ")"
    )
    db.connection.commit()

    db.execute("CREATE TABLE IF NOT EXISTS conversations(" \
            "id INTEGER PRIMARY KEY AUTOINCREMENT," \
            "title TEXT" \
        ")"
    )
    db.connection.commit()

    db.execute("CREATE TABLE IF NOT EXISTS conversation_members(" \
            "conversationId INTEGER PRIMARY KEY AUTOINCREMENT," \
            "userId INTEGER" \
        ")"
    )
    db.connection.commit()
    return DbResult(True, True)
    
    