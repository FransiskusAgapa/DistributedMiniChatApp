# =============================
# Mini Chat App - Tkinter GUI Client
# =============================

import socket          # For networking (connect to server)
import threading       # For sending and receiving at the same time
import tkinter as tk    # For GUI
from tkinter import scrolledtext  # For scrollable chat window
from tkinter import messagebox    # For popup errors

# ======== Configuration ========
HOST = '127.0.0.1'  # Server IP
PORT = 12345        # Server Port

# ======== Create Client Socket ========
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# ======== GUI Setup ========
window = tk.Tk()
window.title("Mini Chat Client 💬")  # Window title
window.geometry("400x500")           # Set fixed window size
window.resizable(False, False)       # Prevent resizing

# ======== GUI Components ========

# Chat log (scrollable text area)
chat_log = scrolledtext.ScrolledText(window, state='disabled', wrap=tk.WORD)
chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Text input field
message_entry = tk.Entry(window)
message_entry.pack(padx=10, pady=(0,10), fill=tk.X)

# Send button
send_button = tk.Button(window, text="Send", command=lambda: send_message())
send_button.pack(padx=10, pady=(0,10))

# Connection label
connection_label = tk.Label(window, text="🔴 Disconnected", fg="red")
connection_label.pack(padx=10, pady=(0,5))

# ======== Functions ========

def connect_to_server():
    """
    Connect to the server and send the username.
    Start a thread to receive messages.
    """
    try:
        client.connect((HOST, PORT))
    except Exception as e:
        messagebox.showerror("Connection Error", f"Cannot connect to server: {e}")
        window.destroy()
        return

    username = simple_prompt("Enter your username:")
    if not username:
        window.destroy()
        return

    client.send(username.encode('utf-8'))

    # Update connection status
    connection_label.config(text="🟢 Connected", fg="green")

    # Start a thread to receive incoming messages
    threading.Thread(target=receive_messages, daemon=True).start()

def simple_prompt(prompt_text):
    """
    Simple input popup to get username.
    """
    popup = tk.Toplevel()
    popup.title("Username")
    popup.geometry("300x100")
    popup.resizable(False, False)

    tk.Label(popup, text=prompt_text).pack(pady=5)
    entry = tk.Entry(popup)
    entry.pack(pady=5)

    result = {"username": None}

    def submit():
        result["username"] = entry.get()
        popup.destroy()

    tk.Button(popup, text="Submit", command=submit).pack()

    # Wait until window closes
    popup.grab_set()
    window.wait_window(popup)

    return result["username"]

def receive_messages():
    """
    Receive messages from server and display them.
    """
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                display_message(message)
            else:
                break
        except:
            break

def send_message():
    """
    Send a message typed by user to the server.
    """
    message = message_entry.get()
    if message:
        try:
            client.send(message.encode('utf-8'))
            message_entry.delete(0, tk.END)  # Clear input field
        except:
            messagebox.showerror("Error", "Failed to send message.")
            client.close()
            window.destroy()

def display_message(message):
    """
    Display a new message in the chat log.
    """
    chat_log.config(state='normal')         # Allow editing
    chat_log.insert(tk.END, message + '\n')  # Insert message
    chat_log.config(state='disabled')        # Make read-only again
    chat_log.yview(tk.END)                   # Auto-scroll to latest message

def on_closing():
    """
    Gracefully close socket when window is closed.
    """
    try:
        client.close()
    except:
        pass
    window.destroy()

# ======== Run Everything ========
window.protocol("WM_DELETE_WINDOW", on_closing)  # Handle window closing
connect_to_server()
window.mainloop()
