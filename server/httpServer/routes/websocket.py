from fastapi import APIRouter, WebSocket, Query, WebSocketDisconnect, WebSocketException

from server.httpServer.auth.rt_session import check_if_valid_rts_token

from server.ws.objects.client import Client


websocket_router = APIRouter(prefix="/ws")

@websocket_router.websocket("/")
async def websocketMain(websocket: WebSocket, token: str = Query(...)) -> str:

    try:
        await websocket.accept()
        if (not await check_if_valid_rts_token(token)):
            await websocket.close()
            return
        
        client = Client(websocket)
     
        while True:
            await client.receiveMsg()
            
            
      
    except WebSocketDisconnect:
        print("websocket disconnected")
    except WebSocketException:
        print("websocket exception")
        await websocket.close()
    except Exception as e:
        print(f"Exception in websocketMain: {e}")
        await websocket.close()
        
        


