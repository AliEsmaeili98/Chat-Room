import socket, threading, os, sys, importlib
import mycolors

nickname = input(mycolors.mycolors.Magenta + "Choose your nickname: " + mycolors.mycolors.Default)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 21000))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == "NICK":
                client.send(nickname.encode('ascii'))
            elif message == "NICKTKN":
                print(mycolors.mycolors.Red + "Nickname Taken!" + mycolors.mycolors.Default)
                client.close
                break
            else:
                print(message)
        except:
            print(mycolors.mycolors.Red + "An error occurred!" + mycolors.mycolors.Default)
            client.close()
            break
    os.execv(sys.executable, ['python'] + sys.argv)

def write():
    while True:
        message = f'{mycolors.mycolors.Green}{nickname}{mycolors.mycolors.Default}: {mycolors.mycolors.LightRed}{input("")}{mycolors.mycolors.Default}'
        client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()