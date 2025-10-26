import websockets.sync.server as websockets
from websockets.sync.server import serve
from .globals import *


class Server:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

        self.server: websockets.Server = None


        self.SHUTDOWN = False

    
    def run_server(self):
        server = serve(self.clientHandler, host="0.0.0.0", port=self.port)
        try:
            
            print(f"Server started... on port {self.port}")
            server.serve_forever()
        finally:
            self.SHUTDOWN = True
            server.server_close()
    
        

    def clientHandler(self, connection: websockets.ServerConnection):
        print(f"Client connected!")
        
        try:
            
            data = connection.recv()
            connection.send(f"Echo: {data}")
        except websockets.ConnectionClosed:
            print("Connection closed dirty")
        finally:
            print("disconnecting...")
            connection.close()
            print("disconnected")
            
            
            

        
            