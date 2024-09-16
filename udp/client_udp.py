import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

addr = ("127.0.0.1", 12345)

message = bytes("Hello, UDP server", 'utf-8')
client_socket.sendto(message, addr)

data, addr = client_socket.recvfrom(4096)

print("Server says")
print(str(data.decode('utf-8')))
client_socket.close()