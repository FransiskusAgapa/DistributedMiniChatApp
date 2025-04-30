# =============================
# Mini Chat App - Tkinter GUI Client
# =============================

import socket                     # Lets us connect to a server using internet
import threading                  # Lets the app send and receive at the same time
import tkinter as tk              # GUI library to build the app window
from tkinter import scrolledtext  # Adds a scrollable text box for messages
from tkinter import messagebox    # Shows popup messages for errors

# ======== Configuration ========
HOST = '127.0.0.1'  # Server IP address (127.0.0.1 means local computer)
PORT = 12345        # The port number used to talk to the server

# ======== Create Client Socket ========
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creates the internet connection tool

# ======== GUI Setup ========
window = tk.Tk()                                  # Start the app window
window.title("Mini Chat Client 💬")               # Set the window title
window.geometry("400x500")                        # Set fixed window size
window.resizable(False, False)                    # Make the window not resizable

# ======== GUI Components ========

# Scrollable box that shows all chat messages
chat_log = scrolledtext.ScrolledText(window, state='disabled', wrap=tk.WORD)
chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)  # Add it to the window

# Text input box where user types their message
message_entry = tk.Entry(window)
message_entry.pack(padx=10, pady=(0,10), fill=tk.X)  # Add to window
message_entry.bind("<Return>", lambda event: send_message())  # Pressing Enter = send message

# "Send" button for sending message
send_button = tk.Button(window, text="Send", command=lambda: send_message())
send_button.pack(padx=10, pady=(0,10))  # Add to window

# Label at the bottom to show if connected or not
connection_label = tk.Label(window, text="🔴 Disconnected", fg="red")
connection_label.pack(padx=10, pady=(0,5))  # Add to window

# ======== Functions ========

def connect_to_server():
    """
    Connects the app to the chat server and starts listening for messages.
    """
    try:
        client.connect((HOST, PORT))  # Try to connect to the server
    except Exception as e:
        messagebox.showerror("Connection Error", f"Cannot connect to server: {e}")  # Show error popup
        window.destroy()  # Close app if failed
        return

    username = simple_prompt("Enter your username:")  # Ask for username
    if not username:
        window.destroy()  # Close if username is empty
        return

    client.send(username.encode('utf-8'))  # Send username to server

    connection_label.config(text="🟢 Connected", fg="green")  # Update status to connected

    threading.Thread(target=receive_messages, daemon=True).start()  # Start listening for messages in background

def simple_prompt(prompt_text):
    """
    Small popup that asks the user to enter their name.
    """
    popup = tk.Toplevel()                 # Create popup window
    popup.title("Username")              # Set title
    popup.geometry("300x100")            # Set size
    popup.resizable(False, False)        # Don't allow resizing

    tk.Label(popup, text=prompt_text).pack(pady=5)  # Label asking for name
    entry = tk.Entry(popup)                         # Input box
    entry.pack(pady=5)

    result = {"username": None}  # Store result inside a dictionary

    def submit():
        result["username"] = entry.get()  # Get the entered name
        popup.destroy()                   # Close popup

    tk.Button(popup, text="Submit", command=submit).pack()  # Button to confirm name

    popup.grab_set()         # Freeze other windows until this one closes
    window.wait_window(popup)  # Wait for popup to close

    return result["username"]  # Return the name

def receive_messages():
    """
    Waits for messages from the server and displays them.
    """
    while True:
        try:
            message = client.recv(1024).decode('utf-8')  # Get message from server
            if message:
                display_message(message)  # Show it in the chat window
            else:
                break  # Server closed
        except:
            break  # Some error happened

def send_message():
    """
    Takes what user typed and sends it to the server.
    """
    message = message_entry.get()  # Get text from input box
    if message:
        try:
            client.send(message.encode('utf-8'))     # Send to server
            message_entry.delete(0, tk.END)          # Clear the box after sending
        except:
            messagebox.showerror("Error", "Failed to send message.")  # Show error popup
            client.close()
            window.destroy()

def display_message(message):
    """
    Adds a message to the chat window.
    """
    chat_log.config(state='normal')              # Allow edits
    chat_log.insert(tk.END, message + '\n')      # Add message at the end
    chat_log.config(state='disabled')            # Make it read-only again
    chat_log.yview(tk.END)                       # Scroll to the latest message

def on_closing():
    """
    Cleanly closes connection when the user closes the app window.
    """
    try:
        client.close()  # Close the socket
    except:
        pass
    window.destroy()    # Close the app window

# ======== Run Everything ========
window.protocol("WM_DELETE_WINDOW", on_closing)  # Make the close button call our cleanup function
connect_to_server()  # Connect and start chatting
window.mainloop()    # Keep the app running (Tkinter loop)
