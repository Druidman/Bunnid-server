from typing import Generic, TypeVar, Optional
import asyncpg
import asyncio
from functools import wraps

T = TypeVar("T")
class DbResult(Generic[T]):
    error: str = ""
    result: Optional[T] = None
    resultJsonable: list[asyncpg.Record] = None
    def __init__(self, result: Optional[T] = None, error: str = ""):
        self.error = error
        self.result = result
       

    def makeResultJsonable(self) -> bool:
        if not self.result: return False

        if type(self.result) == asyncpg.Record:
            self.resultJsonable = [dict(self.result)]
        elif type(self.result) == list[asyncpg.Record]:
            self.resultJsonable = [dict(x) for x in self.result]
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
                return DbResult[None](error=e.__str__())
        return async_logic
    else:
        @wraps(func)
        def sync_logic(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                return DbResult[None](error=e.__str__())
        return sync_logic
