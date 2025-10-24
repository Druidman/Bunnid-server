import sqlite3

DB_RESULT = lambda status ,msg : {
    "STATUS": status,
    "MSG": msg
}


def dbFunction(func):
    def logic(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except sqlite3.Error as e:
            return DB_RESULT(False, e)
    return logic