import socket
from websockets.sync.client import connect


WS_SERVER = "ws://localhost:8080/ws"

with connect(WS_SERVER) as websocket:
    while True:
        message = websocket.recv()
        message = message
        print(f"Received: {message}")
        if message.find("Wrong answer!") != -1 or message.find("flag") != -1:
            break
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # nginx on 80
        s.connect(("localhost", 80))
        s.send(message.encode())
        resp = s.recv(4096).decode()
        status = resp.split("\n")[0].split(" ")[1]
        print(f"Sending: {status}")
        websocket.send(status)