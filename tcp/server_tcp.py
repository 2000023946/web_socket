import socket
import sys
"""
TCP Client side code 
where the socket is made 
and connects to given PORT and SERVER
"""
# # set up tcp with type= socket.SOCKET_STREAM
# try:
#     sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
# except socket.error as err:
#     print("Failed to establish socket!")
#     print(f"Reason: {err}")
#     sys.exit()
# print("Socket Created!")

# target_host = input("Enter the target host to connect: ")
# target_port = input("Enter the target port to connect: ")

# try:
#     sock.connect((target_host, int(target_port)))
#     print("Socket succesfully connected to %s on port: %s"%(target_host, target_port))
# except socket.error as err:
#     print("Failed to connect to %s on port: %s"%(target_host, target_port))
#     print("Reason: %s"%str(err))
#     sys.exit()
"""
TCP SERVER code 
"""
server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
#binds to server and port (server, port)
server = '127.0.0.1'
#port is int and ranges from 1-65,535
port = 12345 
tuple_addr = (server, port)
server_socket.bind(tuple_addr)
# optional param(backlog) max 
#number of clients accpeted by the server
server_socket.listen(5)
#start accpeting incoming connections
while True:
    print("server waiting for connection")
    #accept the client and returns two values 
    #1) socket instance 
    #2) addresss of the client ->
    #tuple(server, port)
    try:
        client_socket, addr = server_socket.accept()
        print("client connected from %s"%str(addr))
    except:
        print("\nServer crashed!")
        sys.exit()
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print("recived from client: %s"%(data.decode('utf-8')))
        try:
            #to send to client all msg conver to byte
            msg = b"Hello Client"
            client_socket.send(msg)
        except KeyboardInterrupt:
            print('Server crashed!')
    client_socket.close()
server_socket.close()

"""
server socket is listening socket 
that binds to server and port by socket.bind()
uses -> accept request from clients
not used -> data transfer between client and server

client connects -> connection has been established
client_socket, address = __server__.socket.accept()
(instance, (server, port))
client_socket is used for the data communication 
of that client and the server

for every client that makes a connection an new 
client instance is made for that client communication
"""
    