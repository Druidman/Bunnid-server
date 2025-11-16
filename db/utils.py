import sqlite3
from typing import List

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
        if not self.msg: return False
        
        if type(self.msg) == sqlite3.Row:
            self.msgDict = dict(self.msg)
            print(f"reulat {self.msgDict}")
        elif type(self.msg) == list and type(self.msg[0]) == sqlite3.Row:

            self.msgDict = [dict(x) for x in self.msg]
            print(f"list {self.msgDict}")
        else:
            return False
        
        return True


        



def dbFunction(func) -> DbResult:
    def logic(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except sqlite3.Error as e:
            return DbResult(False, e)
    return logic
