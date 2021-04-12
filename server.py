import threading, socket, mycolors

# Connection data.
host = "127.0.0.1"
port = 21000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creating a TCP socket for server
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # This command prevents the "Address in use" Error. 
server.bind((host, port)) # Binding host and port together.
server.listen()

# Lists for clients and their nicknames.
clients = []
nicknames = []

# Sending messages to all connected clients.
def broadcast(message):
    for client in clients:
        client.send(message)

# Handling messages from clients.
def handle(client):
    while True:
        try:
            # Receiving messages from clients and creating a string and a list for later use.
            message = client.recv(1024)
            messagestr = message.decode("utf-8")
            messagelist = message.decode("utf-8").split()

            # Checking to see if the client needs a list of users and sending it to him/her if needed.
            if "LIST" in messagelist:
                client.send(f"{mycolors.mycolors.LightBlue}Here is the list of attendees: \n{mycolors.mycolors.Default}".encode('ascii'))
                client.send(f"{mycolors.mycolors.Cyan}, {mycolors.mycolors.Default}".join(map(str, nicknames)).encode('ascii'))

            # Checking to see if the client wants to leave the chatroom and removing his data if needed.
            elif messagelist[1] == "Bye.":
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]

                # Letting everyone know that the client left the server.
                broadcast(f"{mycolors.mycolors.Yellow}{nickname} Left the chat!{mycolors.mycolors.Default}".encode('ascii'))
                print(f"{nickname} Left the server!")

                nicknames.remove(nickname)     
                break

            # If the message is none of above then it's a typical message which we send to clients depending on structure of the message.
            else:

                # Checking to see if the message includes a mention. Due to project description clients always need to identify  who they are messaging.
                if "@" in messagestr:

                    # Checking too see if the client wants to send a public or private message .
                    
                    # Public message.
                    if "@everyone" in messagestr:
                        broadcast(message)

                    #private message .   
                    else:
                        try:

                            # Going through message coverted to a list.
                            for x in range(len(messagelist)):

                                # Checking to see if list items are mentions.
                                if "@" in messagelist[x]:

                                    # Checking to see if the mention is a client and if he/she is a client server sensds the message to them
                                    if messagelist[x].replace("@", "") in nicknames:

                                        # Sending message to client itself.
                                        client.send(message)

                                        pvindex = nicknames.index(messagelist[x].replace("@", ""))
                                        clients[pvindex].send(message)

                                    # If the mention is not a user return a message.   
                                    else:
                                        client.send(f"{mycolors.mycolors.Red}User {messagelist[x].replace('@', '')} Not Found{mycolors.mycolors.Default}".encode('ascii'))
                        except:
                            client.send(f"{mycolors.mycolors.Red}Wrong message format!{mycolors.mycolors.Default}".encode('ascii'))
                else:
                    client.send(f"{mycolors.mycolors.Red}Wrong message format! You have to mention other users!{mycolors.mycolors.Default}".encode('ascii'))
        
        # If the user disconnects without using 'Bye.' command server will let everyone know that he/she disconnected and removes its data.
        except:
            try:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast(f"{mycolors.mycolors.Yellow}{nickname} left the chat!{mycolors.mycolors.Default}".encode('ascii'))
                print(f"{nickname} Left the server!")
                nicknames.remove(nickname)
                break
            except:
                pass

# Receiving/Listening function
def receive():
    while True:

        # Accepting all connections.
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        # Request and store nickname
        client.send("NICK".encode('ascii'))
        nickname = client.recv(1024).decode('ascii')

        # Checking to see if entered nickname is laready used. If not it will create the nickname and let everyone know the new client is connected.
        if not nickname in nicknames:   
            nicknames.append(nickname)
            clients.append(client)
            print(f"Nickname of the client is {nickname}!")
            client.send(f"{mycolors.mycolors.Cyan}Welcome to the ChatRoom {nickname}! Send LIST for the list of online Users.{mycolors.mycolors.Default}\n".encode('ascii'))
            broadcast(f"{mycolors.mycolors.LightBlue}{nickname} joined the chat!{mycolors.mycolors.Default}".encode('ascii'))

        # If nickname is taken it sends a message letting the client script know.    
        else:
            client.send("NICKTKN".encode('ascii'))
        
        # Creating a thread for handle function to acrivly listen to messages.
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is listening...")

# Starting the main function for server.
receive()