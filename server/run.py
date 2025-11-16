from server.httpServer import run_http_server
from server.wsServer import run_ws_server
from server import globals
from server.db import connectDb



if __name__ == "__main__":
    globals.dbConn = connectDb()
    if not globals.dbConn:
        print("Error when connecting to db!")
        exit()
    print("Db succesfully connected")

    run_ws_server()
    

    run_http_server()
    