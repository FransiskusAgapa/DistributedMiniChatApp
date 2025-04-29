# =============================
# Mini Chat App - Client (Fully Commented)
# =============================

import socket     # Import socket library to handle network communication
import threading  # Import threading to handle sending and receiving at the same time

# ======== Configuration ========
HOST = '127.0.0.1'  # Server IP address (localhost for testing)
PORT = 12345        # Port number to connect to the server

# ======== User Setup ========
username = input("Enter your username: ")  # Prompt the user to input a username for identification

# Create a TCP/IP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the chat server
client.connect((HOST, PORT))

# Immediately send the username after connecting
client.send(username.encode('utf-8'))

# ======== Receive Messages Thread ========
def receive_messages():
    """
    Continuously receive and print messages from the server.
    Runs in a separate thread so it doesn't block sending messages.
    """
    while True:
        try:
            # Receive message from server
            message = client.recv(1024).decode('utf-8')
            print(message)  # Print the message to the console
        except:
            # Handle server disconnection or network error
            print("[!] Error: Connection closed by the server.")
            client.close()  # Close the socket
            break

# ======== Send Messages Thread ========
def send_messages():
    """
    Continuously read user input and send it to the server.
    Runs in a separate thread to allow simultaneous sending and receiving.
    """
    while True:
        message = input('')  # Read user input (blocking call)
        client.send(message.encode('utf-8'))  # Send the typed message to the server

# ======== Start Threads ========
# Create and start a thread to receive messages
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Create and start a thread to send messages
send_thread = threading.Thread(target=send_messages)
send_thread.start()
