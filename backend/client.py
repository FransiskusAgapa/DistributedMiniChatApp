# =============================
# Mini Chat App - Client (Simple Version with Comments)
# =============================

import socket     # Lets this program connect to the server through the internet
import threading  # Lets the program do two things at once (send and receive)

# ======== Configuration ========
HOST = '127.0.0.1'  # IP address of the server (127.0.0.1 = your own computer)
PORT = 12345        # The port number the server is using

# ======== User Setup ========
username = input("Enter your username: ")  # Ask the user for their name to show in the chat

# Create a new internet socket to talk to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect this client to the server
client.connect((HOST, PORT))

# Send the username to the server as the first message
client.send(username.encode('utf-8'))

# ======== Receive Messages Thread ========
def receive_messages():
    """
    Runs in the background and keeps checking for new messages from the server.
    When it gets a message, it shows it in the console.
    """
    while True:
        try:
            message = client.recv(1024).decode('utf-8')  # Receive message and turn it into text
            print(message)  # Show the message in your terminal
        except:
            # If there's a problem (like the server disconnects), show an error
            print("[!] Error: Connection closed by the server.")
            client.close()  # Close this client's connection
            break  # Stop this loop

# ======== Send Messages Thread ========
def send_messages():
    """
    Runs in the background and keeps waiting for the user to type a message.
    When the user presses Enter, it sends that message to the server.
    """
    while True:
        message = input('')  # Wait for the user to type something and press Enter
        client.send(message.encode('utf-8'))  # Send that message to the server as bytes

# ======== Start Threads ========

# Create a new thread to handle receiving messages, and start it
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Create a new thread to handle sending messages, and start it
send_thread = threading.Thread(target=send_messages)
send_thread.start()

