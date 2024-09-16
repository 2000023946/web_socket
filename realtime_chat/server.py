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

class Client:
    __all_clients = set()
    __usernames = set()
    @classmethod
    def __increment(cls, inst):
        cls.__all_clients.add(inst)
        cls.__usernames.add(inst.__username)
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


def send_msg(receiver, sender_name, data):
    socket = receiver.get_socket
    socket.send(f"Client {sender_name} sent to everyone: {data}".encode('utf-8'))
    print(f'Message {data} send to {receiver.get_username} from {sender_name}')

def handle_client(socket, addr):
    username = socket.recv(1024).decode('utf-8')
    while username in Client.get_all_usernames():
        socket.send("Username in use. Re-enter your username".encode('utf-8'))
        username = socket.recv(1024)
        username = username.decode('utf-8')
    socket.send("pass".encode('utf-8'))

    new_client = Client(username, addr[1], socket)
    print("Connected to {} on port: {}".format(*addr))
    msg = f"Welcome {new_client.get_username} to server: {new_client.get_port}".encode('utf-8')
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
                        print('loopinh')
                        thread = threading.Thread(target=send_msg, args=(client,new_client.get_username, data['msg']))
                        thread.start()
                        print("thread started")
            socket.send(bytes("Message Recieved", 'utf-8'))
            print(f"From port {port} Client {new_client.get_username} sent: {data['msg']}")
        except OSError:
            break
    socket.close()
        
    
def start():
    server_socket.listen()
    print("[LISTENING] on {} port: {}".format(*tuple_addr))
    while True:
        try:
            client, addr = server_socket.accept()
            
            thread = threading.Thread(target=handle_client, args=(client,addr))
            thread.start()

        except KeyboardInterrupt:
            Client.remove('all')
            print("\nserver is closing down...")
            client.close()
            server_socket.close()
            sys.exit()
    server_socket.close()
start()
