import socket
import sys
import json
#create the socket instance
client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

#use the same port server is running on
#(IP, PORT)
IP = "127.0.0.1"
PORT = 12345
tuple_addr = (IP, PORT)

client_socket.connect(tuple_addr)

try:
    username = input("What would you like your username to be?\n")
    while True:
        client_socket.send(username.encode('utf-8'))
        msg = client_socket.recv(1024)
        if msg.decode('utf-8') == 'pass':
            break
        username = input(msg.decode('utf-8')+"\n")
except socket.error as err:
    print(f"Internal Error\nReason: {err}")
    sys.exit()

def recv_data():
    data = client_socket.recv(1024)
    if data is not None:
        print(str(data.decode('utf-8')))
    return 

try:
    while True:
        recv_data()
        more = input("Would you like to send data?\n")
        if more.lower() == 'yes':
            payload = input("Enter the message.\n")
            to_whom = input("Enter 'all' to send to everyone in the server. And 'user' to send to a specific user.\n")
            if to_whom == 'all':
                dict = {"to":"all", "msg":payload}
                client_socket.send(json.dumps(dict).encode('utf-8'))
except KeyboardInterrupt:
    dict = {"to":"", "msg":"left"}
    client_socket.send(json.dumps(dict).encode('utf-8'))
    print("\nClient has left")
client_socket.close()