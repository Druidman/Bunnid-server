from typing import Callable, Generic, ParamSpec, TypeVar, Optional, Union
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
            self.resultJsonable = dict(self.result)
        elif type(self.result) == list and len(self.result) > 0 and type(self.result[0]) == asyncpg.Record:
            self.resultJsonable = [dict(x) for x in self.result]
        else:
            return False
        
        return True


        

P = ParamSpec("P")
R = TypeVar("R")

def dbFunction(func: Callable[P, R]) -> Callable[P, R]:
    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def async_logic(*args, **kwargs) -> "DbResult[R]":
            try:
                result: DbResult[R] = await func(*args, **kwargs)
                return result
            except Exception as e:
                return DbResult[None](error=e.__str__())
        return async_logic
    else:
        @wraps(func)
        def sync_logic(*args, **kwargs) -> DbResult[R]:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                return DbResult[None](error=e.__str__())
        return sync_logic

