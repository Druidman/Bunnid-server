import requests, json
from websockets.sync.client import connect
import server.wsServer.wsComms as comms
print("TEST START")
httpTest = requests.get("http://127.0.0.1:5000/api/auth/")
print(f"Result of httpServer auth: {httpTest.text}")

token = "loNnNK1TUqjkZipUcLYL"

with connect("ws://127.0.0.1:8080") as connection:
    msg = connection.recv()  
    msg = json.loads(msg)  
    print(f"Received: {str(msg)}, from server")
    if msg["TYPE"] == comms.REQUEST_TOKEN_MSG_REQ_TYPE:
        connection.send(json.dumps(comms.REQUEST_TOKEN_MSG({"TOKEN": token})))
        msg2 = connection.recv()  
        msg2 = json.loads(msg2)  
        print(f"Received: {str(msg2)}, from server")
    
    connection.close()
    

print("TEST END")

