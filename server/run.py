from server.httpServer import run_http_server
# from server.wsServer import run_ws_server
import server.globals as globals
from server.db import setup_db
from server.eventPool import setupEventPool
from server.eventPool.EventType import EventType
import asyncio


async def setup():
    await setup_db() # connects db
    
    setupEventPool() # setup events


def main():
    asyncio.run(setup())

    # run_ws_server() # run websocket RT server
    run_http_server() # run bunnid api


if __name__ == "__main__":
    
    main()
    