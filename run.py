from server.httpServer import run_http_server
from server.wsServer import run_ws_server
from server import globals
from server.db import connectDb
from threading import Thread



if __name__ == "__main__":
    globals.dbConn = connectDb()
    if not globals.dbConn:
        print("Error when connecting to db!")
        exit()
    print("Db succesfully connected")
    
    ws_server_thread = Thread(target=run_ws_server, daemon=True)
    ws_server_thread.start()

    run_http_server()
    