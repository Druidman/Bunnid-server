import sqlite3

class DbResult:
    status: bool = False
    msg = None
    def __init__(self, status: bool, msg):
        self.status = status
        self.msg = msg
        



def dbFunction(func) -> DbResult:
    def logic(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except sqlite3.Error as e:
            return DbResult(False, e)
    return logic
