import socket

client = socket.socket()

host = "127.0.0.1"

port = 12345
print("waiting for connection")
try:
    client.connect((host,port))
except socket.error as err:
    print(str(err))

resp = client.recv(1024)
print(str(resp.decode('utf-8')))
while True:
    data = input("give data to send to server\n")
    client.send(data.encode('utf-8'))
    resp = client.recv(1024)
    print(str(resp.decode('utf-8')))
client.close()