import socket
from threading import Thread

#Socket Method has 2 parameters: 1. Address Family(ip v4), 2. Socket Type(TCP, UDP)
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address='127.0.0.1'
port=8000

server.bind((ip_address, port))
server.listen()

list_of_clients=[]
nicknames=[]
print('Server has started...')

def client_thread(connection, nickname):
    connection.send('Welcome to this Chat Room'.encode('utf-8'))
    while True:
        try:
            message=connection.recv(2048).decode('utf-8')
            if message:
                print(message)
                broadcast(message, connection)
            
            else:
                remove(connection)
                remove_nickname(nickname)
        
        except:
            continue

def broadcast(message, connection):
    for clients in list_of_clients:
        if clients !=connection:
            try:
                clients.send(message.encode('utf-8'))

            except:
                remove(clients)
            
def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

def remove_nickname(nickname):
    if nickname in nicknames:
        nicknames.remove(nickname)

while True:
    connection, address=server.accept()
    connection.send('NICKNAME'.encode('utf-8'))
    nickname=connection.recv(2048).decode('utf-8')
    list_of_clients.append(connection)
    nicknames.append(nickname)
    message='{} joined'.format(nickname)
    print(message)
    broadcast(message,connection)
    new_thread=Thread(target=client_thread, args=(connection, address))
    new_thread.start()