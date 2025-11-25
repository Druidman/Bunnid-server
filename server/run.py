from server.httpServer import run_http_server
from server.wsServer import run_ws_server
import server.globals as globals
from server.db import setup_db
from server.eventPool import setupEventPool
from server.eventPool.EventType import EventType



if __name__ == "__main__":
    setup_db() # connects db
    
    setupEventPool() # setup events

    run_ws_server() # run websocket RT server
    
    run_http_server() # run bunnid api
    