# server.py
# This is the code for the server side of the console chat
# It creates a socket and binds it to the default IP 127.0.0.1 and port 8080
# It listens for incoming connections and creates a new thread for each client
# It receives and broadcasts messages from the clients
# It also handles the nicknames and send times of the clients

import socket
import threading
import time

# Create a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the default IP and port
server.bind((input("IP: "), input("Port: ")))

# Listen for incoming connections
server.listen()

# A list to store the connected clients
clients = []

# A list to store the nicknames of the clients
nicknames = []

# A function to broadcast a message to all the clients
def broadcast(message):
    for client in clients:
        client.send(message)

# A function to handle the communication with a client
def handle(client):
    while True:
        try:
            # Receive a message from the client
            message = client.recv(1024)

            # Broadcast the message to all the clients
            broadcast(message)
        except:
            # Remove the client from the lists if an error occurs
            index = clients.index(client)
            clients.remove(client)
            nickname = nicknames[index]
            nicknames.remove(nickname)

            # Broadcast a message to inform the other clients that the client has left the chat
            broadcast(f'{nickname} left the chat.'.encode('utf-8'))

            # Close the connection with the client
            client.close()

            # Break the loop
            break

# A function to receive new connections
def receive():
    while True:
        # Accept a new connection
        client, address = server.accept()

        # Print the address of the connected client
        print(f'Connected with {str(address)}')

        # Send a message to the client to ask for their nickname
        client.send('NICK'.encode('utf-8'))

        # Receive the nickname from the client
        nickname = client.recv(1024).decode('utf-8')

        # Append the client and the nickname to the lists
        clients.append(client)
        nicknames.append(nickname)

        # Print the nickname of the connected client
        print(f'Nickname of the client is {nickname}')

        # Broadcast a message to inform the other clients that a new client has joined the chat
        broadcast(f'{nickname} joined the chat.'.encode('utf-8'))

        # Send a message to the client to welcome them to the chat
        client.send('You are connected to the server.'.encode('utf-8'))

        # Create a new thread to handle the communication with the client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

# Call the receive function to start the server
receive()
print("Started...")
