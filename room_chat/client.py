import socket
import json
import time 

class PortId:
    __port = 5000
    @classmethod
    def get_port_id(cls):
        cls.__port +=1
        return cls.__port

client = socket.socket()

host = "127.0.0.1"

port = 12345
address = (host, port)
username = input("Enter username: ")
print("waiting for connection")
try:
    client.connect((host,port))
except socket.error as err:
    print(str(err))

resp = client.recv(1024)
print(str(resp.decode('utf-8')))

data = input("join a server\n")
data_dict = {"server_name":data, "username":username}
client.send(json.dumps(data_dict).encode('utf-8'))
msg = client.recv(1024).decode('utf-8')
msg_dict = json.loads(msg)

address = msg_dict['address']

client.close()
time.sleep(1)
new_client = socket.socket()

new_client.connect((address[0], address[1]))

msg = new_client.recv(1024).decode('utf-8')

print(msg)

def recv_data():
    try:
        new_client.setblocking(False)
        new_data = new_client.recv(1024).decode('utf-8')
        new_msg = json.loads(new_data)
        print(f"New Message!")
        print(f"Client {new_msg['username']} sent: {new_msg['msg']}")
    except BlockingIOError:
        print("No new Messages.")
while True:
    try:
        msg = input("What message would you like to send?\n")
        dict_msg = {"username": username, "msg":msg}
        new_client.send(bytes(json.dumps(dict_msg), 'utf-8'))
        recv_data()
    except KeyboardInterrupt:
        new_client.send(bytes(json.dumps({'username': username, "msg":"leave"}), 'utf-8'))
        new_client.close()
        break