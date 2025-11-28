import asyncpg
import asyncio
from functools import wraps
from typing import List

class DbResult:
    status: bool = False
    msg: List[asyncpg.Record] | asyncpg.Record | str | bool = None
    msgAsDbRowObject: bool = False
    msgDict = []
    def __init__(self, status: bool, msg: List[asyncpg.Record] | asyncpg.Record | str | bool, msgAsDbRowObject = False):
        self.status = status
        self.msg = msg
        self.msgAsDbRowObject = msgAsDbRowObject

    def makeMsgDict(self) -> bool:
        if not self.msgAsDbRowObject: return False
        if not self.msg: return False
        
        if type(self.msg) == asyncpg.Record:
            self.msgDict = dict(self.msg)
            print(f"reulat {self.msgDict}")
        elif type(self.msg) == list and type(self.msg[0]) == asyncpg.Record:

            self.msgDict = [dict(x) for x in self.msg]
            print(f"list {self.msgDict}")
        else:
            return False
        
        return True


        



def dbFunction(func) -> DbResult:
    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def async_logic(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                return DbResult(False, e.__str__())
        return async_logic
    else:
        @wraps(func)
        def sync_logic(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                return DbResult(False, e.__str__())
        return sync_logic
