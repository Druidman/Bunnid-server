import websockets.sync.server as websockets
from websockets import ConnectionClosed
from websockets.sync.server import serve
import server.wsServer.wsComms as comms
import json

from server.db.tables.userRTSessions import check_if_token_in_db
import server.globals as globals

from threading import Thread
import time


class Server:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

        self.server: websockets.Server = None


        self.SHUTDOWN = False

    def getMsg(self,connection: websockets.ServerConnection, timeout = None) -> str | None:
        while True:
            try:
                msg = connection.recv(timeout=timeout)
            except:
                return None
            
            return msg

    
    def run_server(self):
        server = serve(self.clientHandler, host="0.0.0.0", port=self.port)
        try:
            
            print(f"Server started... on port {self.port}")
            server.serve_forever()
        finally:
            self.SHUTDOWN = True
            server.server_close()
    
    def authenticateConnection(self, connection: websockets.ServerConnection) -> bool:
        connection.send(json.dumps(comms.REQUEST_TOKEN_MSG()))
        res = self.getMsg(connection, timeout=10)
        if not res:
            return False
        try:
            msg = json.loads(res)
        except:
            return False

        if msg["TYPE"] != comms.REQUEST_TOKEN_MSG_RES_TYPE:
            return False
        
        token = msg["MSG"]["TOKEN"]
        
        dbRes = check_if_token_in_db(token, globals.dbConn.cursor())
        if not dbRes["STATUS"]:
            return False
        
        return dbRes["MSG"]
    
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
        
        pinger = self.startClientPinger(connection)
        try:
            access = False
            if self.authenticateConnection(connection):
                connection.send(json.dumps(comms.ACCESS_GRANTED_MSG))
                access = True
            else:
                connection.send(json.dumps(comms.ACCESS_DENIED_MSG))
                access = False

            while access:
                msg = connection.recv()
                print(f"MSG: {msg}")

            
        except ConnectionClosed:
            print("Connection closed dirty")
        finally:
            
            print("disconnecting...")
            connection.close()
            print("disconnected")
            pinger.join()
            print("connection cleared all up!")
            
            
            

        
            