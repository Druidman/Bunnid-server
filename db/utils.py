import sqlite3

class DbResult:
    status: bool = False
    msg = None
    msgAsDbRowObject: bool = False
    msgDict = []
    def __init__(self, status: bool, msg, msgAsDbRowObject = False):
        self.status = status
        self.msg = msg
        self.msgAsDbRowObject = msgAsDbRowObject

    def makeMsgDict(self) -> bool:
        if not self.msgAsDbRowObject: return False
        self.msgDict = [dict(x) for x in self.msg]
        return True


        



def dbFunction(func) -> DbResult:
    def logic(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except sqlite3.Error as e:
            return DbResult(False, e)
    return logic
