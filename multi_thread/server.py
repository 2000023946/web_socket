"""
two problems
1)cannot handle multiple clients
2)do not know how much data is sent 
(use more accurate buffer capacity)
"""
import socket
import threading
import sys

host = "127.0.0.1"
port = 12345
thread_count = 0

server_socket = socket.socket()

try:
    server_socket.bind((host,port))
except socket.err as err:
    print("Error Occured!")
    print("Reason:", err)
    sys.exit()

server_socket.listen(5)

def client_thread(socket):
    socket.send(str.encode("welcome to server"))
    while True:
        data=socket.recv(2048)
        reply = "hello i am server" + data.decode('utf-8')
        if not data:
            break
        socket.sendall(str.encode(reply))
    socket.close()

while True:
    client, addr = server_socket.accept()
    print("Connected to {} {}".format(*addr))
    threading._start_new_thread(client_thread, (client,))