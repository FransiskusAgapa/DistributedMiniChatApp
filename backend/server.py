import socket       # Lets the server talk over the internet
import threading    # Allows the server to handle many users at once

# ======== Configuration ========
HOST = '127.0.0.1'  # Localhost IP (only works on your own machine)
PORT = 12345        # Port number for chat app (like a door where clients connect)

# ======== Client Management ========
clients = {}        # Dictionary to keep track of users: {client_socket: username}

# ======== Broadcasting Messages ========
def broadcast(message, sender_socket=None):
    """
    Sends a message to all clients (including sender).
    """
    for client in list(clients.keys()):  # Make a copy so we can safely remove items
        try:
            client.send(message.encode('utf-8'))  # Send message as bytes
        except:
            # If sending fails, remove that client
            client.close()
            del clients[client]

# ======== Handle Individual Client ========
def handle_client(client_socket, address):
    """
    Manages one connected user: receives messages, sends them to others.
    """
    try:
        username = client_socket.recv(1024).decode('utf-8')  # First message is the username
        clients[client_socket] = username                    # Store user in dictionary

        # Notify others this user joined
        print(f"[+] {username} has connected from {address}.")
        broadcast(f"🔵 {username} has joined the chat!")
        print(f"[Server] Currently {len(clients)} user(s) connected.")

        # Keep getting messages from this user
        while True:
            message = client_socket.recv(1024).decode('utf-8')  # Read message
            if message:
                print(f"[{username}] {message}")  # Print it on server
                broadcast(f"[{username}] {message}", sender_socket=client_socket)  # Send to others
            else:
                break  # If message is empty, user left

    except:
        # Ignore crashes so server doesn't stop
        pass

    finally:
        # Clean up when user leaves
        if client_socket in clients:
            username = clients[client_socket]                     # Get their name
            print(f"[-] {username} has disconnected.")            # Show they left
            broadcast(f"🔴 {username} has left the chat.")        # Tell others
            del clients[client_socket]                            # Remove from list
        client_socket.close()                                     # Close their connection

# ======== Start Server ========
def start_server():
    """
    Sets up the server and waits for people to join.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Make the server socket
    server.bind((HOST, PORT))                                   # Attach it to IP and port
    server.listen()                                              # Start listening for users

    print(f"[*] Server started on {HOST}:{PORT}")  # Show it's running

    while True:
        client_socket, address = server.accept()  # Wait for someone to join
        thread = threading.Thread(target=handle_client, args=(client_socket, address))  # One thread per user
        thread.start()  # Start talking to that user

# ======== Entry Point ========
if __name__ == "__main__":
    start_server()  # Only run if script is executed (not imported)

