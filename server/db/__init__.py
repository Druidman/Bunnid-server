from .db import *
import server.globals as globals

async def setup_db() -> None:
    print("starting to connect")
    globals.connPool = await connectDb()
    if not globals.connPool:
        print("Error when connecting to db!")
        exit()
    print("Db succesfully connected")