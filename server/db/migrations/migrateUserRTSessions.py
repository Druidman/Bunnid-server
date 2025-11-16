import sqlite3
from ..utils import DbResult, dbFunction

@dbFunction
def migrate_user_RT_sessions(db: sqlite3.Cursor) -> DbResult:
    
    db.execute("CREATE TABLE IF NOT EXISTS UserRTSessions(" \
            "id INTEGER PRIMARY KEY AUTOINCREMENT," \
            "token TEXT," \
            "unique(token)" \
        ")"
    )
    db.connection.commit()
    return DbResult(True, True)
    
    