import sqlite3
from ..utils import DB_RESULT

def migrate_user_sessions(db: sqlite3.Cursor) -> dict:
    try:
        db.execute("CREATE TABLE IF NOT EXISTS UserSessions(" \
                "id INTEGER PRIMARY KEY AUTOINCREMENT," \
                "token TEXT" \
            ")"
        )
        db.connection.commit()
        return DB_RESULT(True, True)
    except sqlite3.Error as e:
        return DB_RESULT(False, e)
    