import socket, threading, mycolors, sys, os

# Temporary nickname for future use.
tempnickname = input(mycolors.mycolors.Magenta + "Choose your nickname: " + mycolors.mycolors.Default)

# Checking to see if the temporary nickname is empty.
if not tempnickname == "":

    # Checking to see if temporary nickname has whitespace. 
    if not " " in tempnickname:
        nickname = tempnickname
    else:
        print(f"{mycolors.mycolors.Red}You can't use whitepsaces in nickname.{mycolors.mycolors.Default}")
        os.execv(sys.executable, ['python'] + sys.argv)  
else:
    print(f"{mycolors.mycolors.Red}You can't leave nickname empty.{mycolors.mycolors.Default}")
    os.execv(sys.executable, ['python'] + sys.argv)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creating a TCP socket for client.
client.connect(('127.0.0.1', 21000)) # Connecting to server.

# Listening to server and sending nickname.
def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')

            # Checking to see if the server is requesting for nickname. 
            if message == "NICK":
                client.send(nickname.encode('ascii'))
            
            # Checking to see if the sent nickname is already taken.
            elif message == "NICKTKN":
                print(mycolors.mycolors.Red + "Nickname Taken!" + mycolors.mycolors.Default)
                client.close
                break

            # If the message is none of the above then we just print the server message for user.
            else:
                print(message)
        
        # If user can't recive messages from server the client sees an error and the client get closed.
        except:
            print(mycolors.mycolors.Red + "An error occurred!" + mycolors.mycolors.Default)
            client.close()
            break

    # If we break out of the while loop it means that the nickname was taken. To take another nickname python script
    # simply restarts with the following code.
    os.execv(sys.executable, ['python'] + sys.argv)

# Sending messages to server.
def write():
    while True:
            message = f'{mycolors.mycolors.Green}{nickname}{mycolors.mycolors.Default}: {input("")}'
            client.send(message.encode('ascii'))

# Creating 2 threads one for receive function and one for write function so they can work at the same time.
receive_thread = threading.Thread(target=receive)
receive_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()