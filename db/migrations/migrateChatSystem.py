import sqlite3
from ..utils import DB_RESULT, dbFunction

@dbFunction
def migrate_chat_system(db: sqlite3.Cursor) -> dict:
    
    db.execute("CREATE TABLE IF NOT EXISTS messages(" \
            "id INTEGER PRIMARY KEY AUTOINCREMENT," \
            "conversationId INTEGER," \
            "receiverId INTEGER," \
            "content TEXT" \
        ")"
    )
    db.execute("CREATE TABLE IF NOT EXISTS conversations(" \
            "id INTEGER PRIMARY KEY AUTOINCREMENT" \
        ")"
    )
    db.execute("CREATE TABLE IF NOT EXISTS conversation_members(" \
            "conversationId INTEGER PRIMARY KEY AUTOINCREMENT," \
            "userId INTEGER" \
        ")"
    )
    db.connection.commit()
    return DB_RESULT(True, True)
    
    