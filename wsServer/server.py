import websockets.sync.server as websockets
from websockets import ConnectionClosed
from websockets.sync.server import serve
import server.wsServer.wsComms as comms
import json

from server.db.tables.userRTSessions import check_if_token_in_db
import server.globals as globals


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
    
    def authenticateConnection(self, connection: websockets.ServerConnection) -> bool:
        connection.send(json.dumps(comms.REQUEST_TOKEN_MSG()))
        res = connection.recv()
        msg = json.loads(res)
        if msg["TYPE"] != comms.REQUEST_TOKEN_MSG_RES_TYPE:
            return False
        
        token = msg["MSG"]["TOKEN"]
        
        dbRes = check_if_token_in_db(token, globals.dbConn.cursor())
        if not dbRes["STATUS"]:
            return False
        
        return dbRes["MSG"]


    def clientHandler(self, connection: websockets.ServerConnection):
        print(f"Client connected!")
        
        try:
            if self.authenticateConnection(connection):
                connection.send(json.dumps(comms.ACCES_GRANTED_MSG))
            else:
                connection.send(json.dumps(comms.ACCES_DENIED_MSG))
                

            
        except ConnectionClosed:
            print("Connection closed dirty")
        finally:
            print("disconnecting...")
            connection.close()
            print("disconnected")
            
            
            

        
            