import socket
#create the socket instance
client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

#use the same port server is running on
#(IP, PORT)
IP = "127.0.0.1"
PORT = 12345
tuple_addr = (IP, PORT)
client_socket.connect(tuple_addr)

payload = "Hey server"

try:
    while True:
        client_socket.send(payload.encode('utf-8'))
        data = client_socket.recv(1024)
        print(str(data.decode('utf-8')))
        more = input("want to pass more data to server?\n")
        if more.lower() == 'yes':
            payload = input("Enter payload\n")
        else:
            break
except KeyboardInterrupt:
    print("\nClient has left")
client_socket.close()