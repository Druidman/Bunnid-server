import sqlite3
from ..utils import DB_RESULT, dbFunction

@dbFunction
def migrate_user_sessions(db: sqlite3.Cursor) -> dict:
    
    db.execute("CREATE TABLE IF NOT EXISTS UserSessions(" \
            "id INTEGER PRIMARY KEY AUTOINCREMENT," \
            "token TEXT," \
            "unique(token)" \
        ")"
    )
    db.connection.commit()
    return DB_RESULT(True, True)
    
    