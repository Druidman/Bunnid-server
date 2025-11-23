from .db import *
import server.globals as globals

def setup_db() -> None:
    globals.dbConn = connectDb()
    if not globals.dbConn:
        print("Error when connecting to db!")
        exit()
    print("Db succesfully connected")