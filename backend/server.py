import socket       # Import socket library to create server socket
import threading    # Import threading to handle multiple clients simultaneously

# ======== Configuration ========
HOST = '127.0.0.1'  # IP address where server will listen (localhost for testing)
PORT = 12345        # Port number to listen on

# ======== Client Management ========
clients = {}        # Dictionary to store client sockets and usernames {socket: username}

# ======== Broadcasting Messages ========
def broadcast(message, sender_socket=None):
    """
    Send a message to all connected clients except the sender.
    Used for chat messages and join/leave notifications.
    """
    for client in list(clients.keys()):
        #if client != sender_socket:
        try:
            client.send(message.encode('utf-8'))  # Encode message as bytes and send
        except:
            # Handle broken client connections
            client.close()
            del clients[client]

# ======== Handle Individual Client ========
def handle_client(client_socket, address):
    """
    Handle communication with a single client.
    Receives username first, then continuously relays messages.
    """
    try:
        # First message from client is their username
        username = client_socket.recv(1024).decode('utf-8')
        clients[client_socket] = username

        # Notify others that a new user has joined
        print(f"[+] {username} has connected from {address}.")
        broadcast(f"🔵 {username} has joined the chat!")
        print(f"[Server] Currently {len(clients)} user(s) connected.")

        # Continuously receive messages from this client
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"[{username}] {message}")  # Log the message on the server side
                broadcast(f"[{username}] {message}", sender_socket=client_socket)
            else:
                break  # Empty message indicates client disconnection

    except:
        # Handle any unexpected errors silently (to avoid server crash)
        pass

    finally:
        # When client disconnects, clean up
        if client_socket in clients:
            username = clients[client_socket]
            print(f"[-] {username} has disconnected.")
            broadcast(f"🔴 {username} has left the chat.")
            del clients[client_socket]
        client_socket.close()

# ======== Start Server ========
def start_server():
    """
    Create the server socket, bind it, and accept incoming client connections.
    Each client is handled in a separate thread.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create TCP socket
    server.bind((HOST, PORT))                                  # Bind to specified IP and port
    server.listen()                                            # Start listening for incoming connections

    print(f"[*] Server started on {HOST}:{PORT}")

    while True:
        client_socket, address = server.accept()                # Accept a new client connection
        thread = threading.Thread(target=handle_client, args=(client_socket, address))  # Handle client in a new thread
        thread.start()  # Start the thread

# ======== Entry Point ========
if __name__ == "__main__":
    start_server()
