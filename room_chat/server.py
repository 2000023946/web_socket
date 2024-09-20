"""
two problems
1)cannot handle multiple clients
2)do not know how much data is sent 
(use more accurate buffer capacity)
"""
import socket
import threading
import sys
import json

host = "127.0.0.1"
port = 12345
thread_count = 0

general_socket = socket.socket()


class PortId:
    __port = 5000
    @classmethod
    def get_port_id(cls):
        cls.__port +=1
        return cls.__port

general_socket.bind((host,port))

general_socket.listen(5)

server_map = {
    
}
pointer = 0
new_servers = []
address = (host, port)

client_map = {}

def client_thread(socket):
    global address
    socket.send(str.encode("welcome to server"))
    data=socket.recv(2048).decode('utf-8')
    print(data)
    data_dict = json.loads(data)
    if not data:
        return
    new_servers.append(data_dict)
    print(new_servers)
    if data_dict['server_name'] in server_map:
        server = server_map[data_dict['server_name']]['server']
        address = server.getsockname()
        socket.send(str.encode(json.dumps({"msg":True, "address":address})))
    else:
        address = (host, PortId.get_port_id())
        socket.send(str.encode(json.dumps({"msg":False, "address":address})))
    socket.close()
    handle_server()
    
msg_map = {}

def send_msg(data, person):
    print(client_map)
    person_socket = client_map[person]
    person_socket.send(json.dumps(data).encode('utf-8'))
    print("message sent")

def new_server_thread(client, name):
    global client_map
    client.send(str.encode(f"Welcome to {name} server"))
    print(server_map)
    print(client_map)
    while True:
        try:
            data = client.recv(1024).decode('utf-8')
            dict_data = json.loads(data)
            msg = dict_data['msg']
            username = dict_data['username']
            username = dict_data['username']
            if msg == 'leave':
                print(f"Client {username} left {name} server")
                return
            print(f"New message on server {name}: {msg}. Sent by {username}")
            for person in server_map[name]['clients']:
                if person is not None and person != username:
                    print(f"Sending message to {person}...")
                    thread = threading.Thread(target=send_msg, args=(dict_data, person))
                    thread.start()
        except OSError:
            client.close()
            server_map[name]['clients'].remove(username)
            client_map[username] = None
            print(client_map)
            print(server_map)


def handle_server():
    global pointer
    if pointer < len(new_servers):
        print("next step", pointer)
        server_dict = new_servers[pointer]
        pointer +=1
        name = server_dict['server_name']
        username = server_dict['username']
        print(name)
        if name is not None:
            print(server_map)
            if name in server_map:
                print(f'has name {name}')
                server = server_map[name]['server']
                client, addr =  server.accept()
                clients = server_map[name]['clients']
                clients.append(username)
                client_map[username] = client
                threading._start_new_thread(new_server_thread, (client,name))
            else:
                new_socket = socket.socket()
                print(address)
                new_socket.bind((address[0], address[1]))
                new_socket.listen()
                client, addr = new_socket.accept()
                print(f"nost has {name}")

                server_map[name] = {"server":new_socket, 'clients': [username]}
                client_map[username] = client
                threading._start_new_thread(new_server_thread, (client,name))


while True:
    client, addr = general_socket.accept()
    print("Connected to {} {}".format(*addr))
    thread = threading.Thread(target=client_thread, args=(client,))
    thread.start()