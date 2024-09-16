import socket

server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
IP = "127.0.0.1"
port = 12345
server_socket.bind((IP, port))

while True:
    data, addr = server_socket.recvfrom(4096)
    print(str(data.decode('utf-8')))
    message = bytes("Welcome to UDP server", 'utf-8')
    server_socket.sendto(message, addr)