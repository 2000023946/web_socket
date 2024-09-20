import socket
import sys
import threading
import json
from random import random
server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
server = '127.0.0.1'
port = 12345
tuple_addr = (server, port)
server_socket.bind(tuple_addr)
server_socket.listen()

class PortId:
    __port = 12345
    @classmethod
    def get_port_id(cls):
        cls.__port +=1
        return cls.__port

class Server:
    __all_codes = {}
    def __init__(self, socket, name, code, limit=None):
        self.__clients = []
        self.__limit = limit
        self.__socket = socket
        self.__code = code
        __class__.__all_codes[self.__code] = self
        self.__name = name
        self.__port = PortId.get_port_id()
        #binds to socket to ip and port 
        self.__socket.bind((server, self.__port))
    def add_client(self, client):
        self.clients.append(client)
    def remove_client(self, client):
        self.clients.remove(client)
    def start_server(self):
        start(self.__socket)
    @property
    def get_socket(self):
        return self.__socket
    @property
    def port(self):
        return self.__port
    @classmethod
    def get_server(cls, code):
        return cls.__all_codes[code]

        

class Client:
    __all_clients = set()
    __usernames = []
    @classmethod
    def __increment(cls, inst):
        cls.__all_clients.add(inst)
        cls.__usernames.append(inst.__username)
    @classmethod
    def get_count(cls):
        return len(cls.__all_clients)
    @classmethod
    def get_all_usernames(cls):
        return cls.__usernames
    @classmethod
    def remove(cls, inst):
        if isinstance(inst, str) and inst == 'all':
            cls.__all_clients.clear()
            return
        cls.__all_clients.remove(inst)
        cls.__usernames.remove(inst.__username)
    @classmethod
    def get_all_clients(cls):
        return cls.__all_clients
    @classmethod
    def get_client(cls, username):
        for client in cls.__all_clients:
            if client.__username == username:
                return client
    @classmethod
    def is_username_valid(cls, username):
        if not username in cls.__usernames:
            return True
        return False
    def __init__(self, username, port, socket):
        self.__username = username
        self.__port = port
        self.__socket = socket
        Client.__increment(self)
    @property
    def get_username(self):
        return self.__username
    @property
    def get_port(self):
        return self.__port
    @property
    def get_socket(self):
        return self.__socket


def send_msg(receiver, sender_name, data, name):
    if receiver is None:
        socket.send(f"Message could not be sent. No client named {name}".encode('utf-8'))
        return
    socket = receiver.get_socket
    socket.send(f"Client {sender_name} sent to {name}: {data}".encode('utf-8'))
    print(f'Message {data} send to {receiver.get_username} from {sender_name}')



def handle_client(socket, addr, server):
    username = socket.recv(1024).decode('utf-8')
    while not Client.is_username_valid(username):
        socket.send("Username in use. Re-enter your username".encode('utf-8'))
        username = socket.recv(1024)
        username = username.decode('utf-8')
    socket.send("pass".encode('utf-8'))
    new_client = Client(username, addr[1], socket)
    print("Connected to {} on port: {}".format(*addr))
    msg = f"Welcome {new_client.get_username} to server: {new_client.get_port}\n".encode('utf-8')
    socket.send(msg)
    print(f"New Client {new_client.get_username} Connected on {addr[0]} port: {addr[1]}")
    print(f'[CONNECTIONS] {Client.get_count()}')
    while True:
        try:
            data  = socket.recv(1024)
            if not data:
                break
            data = data.decode('utf-8')
            data = json.loads(data)
            if data['msg'] == 'left':
                Client.remove(new_client)
                print(f"Client {new_client.get_username} has left the server")
                print(f'[CONNECTIONS] {Client.get_count()}')
                break
            if data['to'] == 'all':
                for client in Client.get_all_clients():
                    if client != new_client:
                        thread = threading.Thread(target=send_msg, args=(client,new_client.get_username, data['msg']))
                        thread.start()
            elif data['to'] =='get_user':
                socket.send(bytes(json.dumps({"users":Client.get_all_usernames()}), 'utf-8'))
            else:
                thread = threading.Thread(target=send_msg, args=(Client.get_client(data['to']),new_client.get_username, data['msg'], data['to']))
                thread.start()
                socket.send(bytes("Message Recieved", 'utf-8'))
                print(f"From port {port} Client {new_client.get_username} sent: {data['msg']}")
        except OSError:
            break
    socket.close()
        

def create_server(client_socket, addr):
    server_data = client_socket.recv(1024).decode('utf-8')
    print(server_data)
    server_dict = json.loads(server_data)
    if server_dict['name'] is None:
        server = Server.get_server(server_dict['code'])
        new_socket = server.get_socket
        client_socket.send(bytes(server.port, 'utf-8'))
        start(new_socket, True)
    else:
        new_server = Server(socket.socket(), server_dict['name'], server_dict['code'])
        new_socket = new_server.get_socket
        start(new_socket, True)
    
    
def start(socket, msg):
    socket.listen()
    print("[LISTENING] on {} port: {}".format(*tuple_addr))
    while True:
        try:
            client_socket, addr = socket.accept()

            if  msg is None:
                server_thread = threading.Thread(target=create_server, args=(client_socket, addr))
                server_thread.start()
            else:
                thread = threading.Thread(target=handle_client, args=(client_socket,addr, server))
                thread.start()
        except KeyboardInterrupt:
            Client.remove('all')
            print("\nserver is closing down...")
            socket.close()
            sys.exit()
    server_socket.close()


start(server_socket, False)
