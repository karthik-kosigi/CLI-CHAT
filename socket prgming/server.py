# import socket

# s = socket.socket()
# print('Socket Created')

# s.bind(('192.168.173.74',9999))

# s.listen(3)
# print('waiting for the connections')

# while True:
#     c, addr = s.accept()
#     name = c.recv(1024).decode()

#     print("connected with ",addr,name)

#     c.send(bytes('welcome to server, you have requested to connect to the server.','utf-8'))
#     c.close()



import socket

# Define the host and port on which the server will listen
HOST = 'localhost'  # This means the server will listen on this specific IP address
PORT = 12345

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(1)

print('Server is listening for incoming connections on', HOST, 'port', PORT)

# Accept a client connection
client_socket, client_address = server_socket.accept()
print('Connected to', client_address)

while True:
    # Receive data from the client
    data = client_socket.recv(1024)
    if not data:
        break
    print('Received:', data.decode())

    # Echo back the received data
    client_socket.sendall(data)

# Close the connection
client_socket.close()
server_socket.close()
