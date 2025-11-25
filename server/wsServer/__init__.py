from .server import Server
from threading import Thread
import os


def run_ws_server():
    serverObj: Server = Server("", int(os.environ.get("PORT", 8080)))
    ws_server_thread = Thread(target=serverObj.run_server, daemon=True)
    ws_server_thread.start()
   
    