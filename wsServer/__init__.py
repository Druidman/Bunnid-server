from .server import Server
from threading import Thread


def run_ws_server():
    serverObj: Server = Server("0.0.0.0", 8080)
    ws_server_thread = Thread(target=serverObj.run_server, daemon=True)
    ws_server_thread.start()
   
    