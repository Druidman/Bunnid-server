import websockets.sync.server as websockets

from websockets.exceptions import InvalidHandshake, ConnectionClosed, InvalidMessage
from websockets.sync.server import serve

import server.globals as globals


from threading import Thread
import time
import http
from server.wsServer.objects.client import Client

from server.eventPool.EventType import EventType


class Server:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

        self.server: websockets.Server = None


        self.SHUTDOWN = False

    def health_check(self, connection: websockets.ServerConnection, request):
        if request.path == "/healthz":
            return connection.respond(http.HTTPStatus.OK, "OK\n")
        return None
    def run_server(self):
        server = serve(self.clientHandler, host=self.host, port=self.port, process_request=self.health_check)
        try:
            
            print(f"Server started... on port {self.port}")
            server.serve_forever()
        finally:
            self.SHUTDOWN = True
            server.server_close()
    
    
    
    def pingConnection(self,connection: websockets.ServerConnection) -> bool:
        try:
            ping_waiter = connection.ping()
        
            return ping_waiter.wait(timeout=10)
        except:
            return False

    def clientPinger(self, connection: websockets.ServerConnection):
        while True:
            if not self.pingConnection(connection): break
            time.sleep(10)
        return 
    
    def startClientPinger(self, connection: websockets.ServerConnection):
        pinger = Thread(target=self.clientPinger, args=(connection,), daemon=False)
        pinger.start()
        return pinger
        

    def clientHandler(self, connection: websockets.ServerConnection):
        print(f"Client connected!")
        
        

        client = Client(connection)

        pinger = self.startClientPinger(connection)
       
        try:
            if not client.authenticate(): return #go to finally
            print("After auth now starting to pool msg'es")
            
            client.msgReceiver()

        except ConnectionClosed:
            print("Connection closed dirty")
        except InvalidHandshake: pass
        except InvalidMessage: pass

        finally:
            
            print("disconnecting...")
            connection.close()
            print("disconnected")
            pinger.join()
            print("connection cleared all up!")
            
            
            

        
            