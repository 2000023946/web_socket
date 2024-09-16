import socket

PORT = 5050
HEADER = 64
FORMAT = 'UTF-8'

DISCONNECT_MESSAGE = "!DISCONNECT"

SERVER = socket.gethostbyname(socket.gethostname())

ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(HEADER).decode(FORMAT))

def run():
    while True:
        msg = input("What message would you like to send?\n")
        send(msg)
        if msg == "leave":
            send(DISCONNECT_MESSAGE)
            break

run()
