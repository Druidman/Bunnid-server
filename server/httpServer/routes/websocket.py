from fastapi import APIRouter, WebSocket, Query, WebSocketDisconnect, WebSocketException

from server.httpServer.auth.rt_session import check_if_valid_rts_token

from server.ws.objects.client import Client
import server.globals as globals


websocket_router = APIRouter(prefix="/ws")

class NotAuthorized(Exception):
    def __init__(self, *args):
        super().__init__(*args)
    
    def __str__(self) -> str:
        return f"Client not authorized to use websocket connection"
    
async def authenticate_client(websocket: WebSocket) -> None:
    try:
        authData = await websocket.receive_json()

        if not globals.validateObject(authData, ["event", "data", "requestId", "error"]):
            raise NotAuthorized
        if not globals.validateObject(authData["data"], ["RTSToken"]):
            raise NotAuthorized
        token = authData["data"]["RTSToken"]
        
        if (not await check_if_valid_rts_token(token)):
            raise NotAuthorized
        
    except:
        raise

@websocket_router.websocket("/")
async def websocketMain(websocket: WebSocket) -> str:

    try:
        await websocket.accept()
        # Auth
        await authenticate_client()
    
        client = Client(websocket)
     
        while True:
            await client.receiveMsg()
            
            
      
    except WebSocketDisconnect:
        print("websocket disconnected")
    except WebSocketException:
        print("websocket exception")
        await websocket.close()
    except NotAuthorized as e:
        print(e.__str__())
        await websocket.close()
    except Exception as e:
        print(f"Exception in websocketMain: {e}")
        await websocket.close()
        
        


