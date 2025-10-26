import requests
from websockets.sync.client import connect
print("TEST START")
httpTest = requests.get("http://127.0.0.1:5000/api/auth/")
print(f"Result of httpServer auth: {httpTest.text}")



with connect("ws://127.0.0.1:8080") as connection:
    connection.send("Hello from test")
    msg = connection.recv()    
    print(f"Received: {str(msg)}, from server")
    connection.close()

print("TEST END")

