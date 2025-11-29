import asyncio
import websockets
import time, json


async def main():
    RTS_TOKEN = "fEJ5Ug-_-d_qq95g7iTv"
    uri = f"ws://localhost:5000/api/ws/?token={RTS_TOKEN}"

    async with websockets.connect(uri) as websocket:  
        try:
            
            while True:
                await websocket.send(json.dumps(
                    {
                        "event": "RT_MESSAGES_IN_CONVERSATION",
                        "error": "",
                        "data": {
                            "conversationId": 0
                        },
                        "requestId": 1
                    }
                ))
                msg = await websocket.recv()
                print("Received:", msg)
                time.sleep(1)
        
            await websocket.close()
        except websockets.ConnectionClosed:
            print("Server closed the connection")
        except websockets.WebSocketException as e:
            print(f"Exception occured on connection: {e.__str__()}")
            print("Shutting down...")
            await websocket.close()
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"EXCEPTION IN WSCONNVCT: {e}")
        

    
    print("End.")

asyncio.run(main())