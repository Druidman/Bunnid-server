import sqlite3
from ..utils import DbResult, dbFunction

@dbFunction
def migrate_users(db: sqlite3.Cursor) -> DbResult:
    db.execute("CREATE TABLE IF NOT EXISTS Users(" \
            "id INTEGER PRIMARY KEY AUTOINCREMENT," \
            "name TEXT," \
            "login TEXT," \
            "password TEXT," \
            "unique(name, login)" \
            
        ")"
    )
    db.connection.commit()
    return DbResult(True, True)
    
    