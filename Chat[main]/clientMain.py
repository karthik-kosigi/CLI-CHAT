import socket
import threading
 

nickname = input('Choose a nickname: ')
if nickname == 'admin':
    password = input("Enter password for admin: ")

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('localhost',55555))

stop_thread = False

def recieve():
    while True:
        global stop_thread 
        if stop_thread:
            break
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                next_message = client.recv(1024).decode('ascii')
                if next_message == 'PASS':
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii') == 'REFUSE':
                        print('Connection was refused! wrong password...')
                        stop_thread = True
                elif next_message == 'BAN':
                    print('Connection refused because of ban!')
                    client.close()
                    stop_thread = True

            else:
                print(message)
        except:
            print("An error occured!")
            client.close()
            stop_thread = True
            break

def write():
    global stop_thread
    while True:
        if stop_thread:
            break

        message = f'{nickname} : {input("")}'
        if message[len(nickname)+3:].startswith('/'):
            if nickname == 'admin':
                if message[len(nickname)+3:].startswith('/kick'):
                    client.send(f'KICK {message[len(nickname)+3+6:]}'.encode('ascii'))
                elif message[len(nickname)+3:].startswith('/ban'):
                    client.send(f'BAN {message[len(nickname)+3+5:]}'.encode('ascii'))
            else:
                print("Command can only be executed by admin")
        elif message[len(nickname)+3:].startswith('quit'):
            print(f'{nickname} has exited the chat!')
            client.send(f'QUIT {nickname}'.encode('ascii'))
            stop_thread = True
            break
        else:
            client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=recieve)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()