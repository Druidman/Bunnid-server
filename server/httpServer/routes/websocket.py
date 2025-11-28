from fastapi import APIRouter, WebSocket, Query, WebSocketDisconnect, WebSocketException

from server.httpServer.auth.rt_session import check_if_valid_rts_token


websocket_router = APIRouter(prefix="/ws")

@websocket_router.websocket("/")
async def serviceMain(websocket: WebSocket, token: str = Query(...)) -> str:
    try:
        await websocket.accept()
        if (not await check_if_valid_rts_token(token)):
            await websocket.close()
            return
        while True:

            data = await websocket.receive_text()
            await websocket.send_text(data)
    except WebSocketDisconnect:
        print("websocket disconnected")
    except WebSocketException:
        await websocket.close()
        print("websocket exception")


