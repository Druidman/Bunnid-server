import sqlite3
from ..utils import DbResult, dbFunction

@dbFunction
def migrate_user_sessions(db: sqlite3.Cursor) -> DbResult:
    
    db.execute("CREATE TABLE IF NOT EXISTS UserSessions(" \
            "id INTEGER PRIMARY KEY AUTOINCREMENT," \
            "token TEXT," \
            "userId INTEGER," \
            "unique(token)" \
        ")"
    )
    db.connection.commit()
    return DbResult(True, True)
    
    