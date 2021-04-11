import threading, socket
import mycolors

host = "127.0.0.1"
port = 21000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host, port)) 
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            word = message.decode("utf-8").split()
            if word[1] == "LIST":
                client.send("-".join(map(str, nicknames)).encode('ascii'))
            else:
                broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{mycolors.mycolors.Yellow}{nickname} left the chat!{mycolors.mycolors.Default}".encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send("NICK".encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        if not nickname in nicknames:   
            nicknames.append(nickname)
            clients.append(client)
            print(f"Nickname of the client is {nickname}!")
            client.send(f"{mycolors.mycolors.Cyan}Welcome to the ChatRoom! Send LIST for the list of online Users.{mycolors.mycolors.Default}\n".encode('ascii'))
            broadcast(f"{mycolors.mycolors.Blue}{nickname} joined the chat!{mycolors.mycolors.Default}".encode('ascii'))
        else:
            client.send("NICKTKN".encode('ascii'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is listening...")
receive()