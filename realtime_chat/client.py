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
username = input("What would you like your username to be?\n")

def get_validated_code():
    while True:
        try:
            code = input("Enter a five digit numerical code to join your server.\n")
            return code
        except ValueError:
            print("Enter a valid numberical code!")

try:
    while True:
        option = input("Enter 'create' or 'join' to a server.\n")
        if option == 'create':
            server_name = input("Enter the name of your server.\n")
            code = get_validated_code()
            dict = {"name":server_name, "code":code, 'to':None, "msg":None}
            print(dict)
            client_socket.send(json.dumps(dict).encode('utf-8'))
            PORT = client_socket.recv(1024).decode('utf-8')
        if option == 'join':
            code = input("Enter the code of the server you want to join.\n")
            dict = {"server_name":None, "code":code, 'to':None, "msg":None}
            client_socket.send(json.dumps(dict).encode('utf-8'))
        client_socket.shutdown(socket.SHUT_RDWR)
        client_socket.close()
        break
except socket.error as err:
    print(f"Internal Error\nReason: {err}")
    sys.exit()

client_socket = socket.socket()
print(PORT)
client_socket.connect((IP, float(PORT)+1))
while True:
    client_socket.send(username.encode('utf-8'))
    msg = client_socket.recv(1024)
    if msg.decode('utf-8') == 'pass':
        break
    username = input(msg.decode('utf-8')+"\n")
            

def recv_data():
    #client_socket.setblocking(False)
    try:
        data = client_socket.recv(1024)
        if data is not None:
            print(str(data.decode('utf-8')))
    except BlockingIOError:
        print("No new messages!")

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
            if to_whom == 'user':
                client_socket.send(bytes(json.dumps({"to":"get_user", 'msg':None}), 'utf-8'))
                data = client_socket.recv(1024)
                if data is not None:
                    data = json.loads(data.decode('utf-8'))
                    users = data['users']
                    print("List of clients:", end="")
                    for user in users:
                        if username != user:
                            print(user, end=", ")
                    user = input(f"\nWhich user would you like to send the message to?\n")
                    dict = {"to":f"{user}", "msg":payload}
                    client_socket.send(json.dumps(dict).encode('utf-8'))
except KeyboardInterrupt:
    dict = {"to":"", "msg":"left"}
    client_socket.send(json.dumps(dict).encode('utf-8'))
    print("\nClient has left")
client_socket.close()