# client.py
# This is the code for the client side of the console chat
# It creates a socket and connects it to the server IP and port
# It sends and receives messages from the server
# It also handles the nicknames and send times of the clients

import socket
import threading
import time

# Create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server IP and port
client.connect((input("IP: "), input("Port: ")))

# A function to receive messages from the server
def receive():
    while True:
        try:
            # Receive a message from the server
            message = client.recv(1024).decode('utf-8')

            # Check if the message is a request for the nickname
            if message == 'NICK':
                # Send the nickname to the server
                client.send(nickname.encode('utf-8'))
            else:
                # Print the message to the console
                print(message)
        except:
            # Print an error message if an error occurs
            print('An error occurred!')

            # Close the connection with the server
            client.close()

            # Break the loop
            break

# A function to send messages to the server
def write():
    while True:
        # Input a message from the user
        message = input('')

        # Get the current time in hours and minutes
        send_time = time.strftime('%H:%M', time.localtime())

        # Format the message with the send time and the nickname
        message = f'[{send_time}]@{nickname}>> {message}'

        # Send the message to the server
        client.send(message.encode('utf-8'))

# Input a nickname from the user
nickname = input('Choose a nickname: ')

# Create a new thread to receive messages from the server
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# Create a new thread to send messages to the server
write_thread = threading.Thread(target=write)
write_thread.start()
